from facebook import FacebookMessenger, Graph
from facebook import MessageElements as Elements
from dialogflow import DialogFlow
from firestore import FireStore
from neis import NEIS
from logger import Logger
from template import Templates

import datetime
import pytz


class Processing:
    def __init__(self, config):
        self.config = config

        self.fm = FacebookMessenger(config)
        self.graph = Graph(config)
        self.df = DialogFlow(config)
        self.fs = FireStore(config)
        self.neis = NEIS(config)

        self.logger = Logger()

        return

    def process_message(self, user, req_str):
        # 1. 타이핑 풍선 띄우기
        self.fm.typing(user)

        # 2. DIALOGFLOW 리퀘스트
        try:
            df_result = self.df.analyze(req_str, user.uid, user.uid + str(user.use_count))
            intent = df_result['queryResult']['intent']['displayName']
        except KeyError as e:
            # Log Error
            self.logger.log('DF KeyError 발생!', 'ERROR', details=str(e))

            # Send Error Message
            reply = '죄송합니다, 급식봇에 오류가 발생했습니다.\n' \
                    '자세한 정보: 언어 분석에 실패했습니다.\n' \
                    '다시 시도해 주시고 오류가 계속되면 아래의 \'버그 신고하기\' 기능을 이용해 주세요.'
            self.fm.send(user.uid, reply, qr=Templates.QuickReplies.after_system_error)
            return
        except Exception as e:
            # 기타 오류
            self.logger.log('DF 기타 오류!', 'ERROR', details=str(e))
            reply = '죄송합니다, 급식봇에 오류가 발생했습니다.\n' \
                    '자세한 정보: 언어 분석에 알 수 없는 이유로 실패했습니다.\n' \
                    '다시 시도해 주시고 오류가 계속되면 아래의 \'버그 신고하기\' 기능을 이용해 주세요.'
            qr = Elements.QuickReply(Templates.QuickReplies.after_system_error)
            self.fm.send(user.uid, reply, qr)
            return

        # 2. Intent 분기
        # Intent: 소스 코드 보기
        if intent == 'Action.SourceCode':
            self.fm.send(user.uid, '급식봇5의 소스는 여기서 보실 수 있어요!')
            card = Elements.Card(Templates.Cards.view_source)
            qr = Elements.QuickReply(Templates.QuickReplies.after_action)
            self.fm.send(user.uid, card, qr)
            return

        # Intent: No
        elif intent == 'Communication.Swear':
            self.fm.send(user.uid, ':(', Templates.QuickReplies.after_user_error)

        # Intent: Yes
        elif intent == 'Communication.Yes':
            self.fm.send(user.uid, ':)', Templates.QuickReplies.default)

        # Intent: 부르기
        elif intent == 'Communication.Calling':
            self.fm.send(user.uid, '네, 여기 있어요.', Templates.QuickReplies.default)

        # Intent: 굿
        elif intent == 'Communication.ThankYou':
            self.fm.send(user.uid, '고마워요!', Templates.QuickReplies.default)

        # Intent: 버그 신고하기
        elif intent == 'Action.Report':
            return self.process_postback(user, 'BUG_REPORT')

        # Intent: 도움말
        elif intent == 'Action.Help':
            return self.process_postback(user, 'HELP')

        # Intent: 인사하기
        elif intent == 'Communication.Hi':
            self.fm.send(user.uid, '안녕하세요!', Templates.QuickReplies.default)

        # Intent: 인사하기
        elif intent == 'Communication.Bye':
            self.fm.send(user.uid, '👋', Templates.QuickReplies.default)

        # Intent: 급식
        elif intent == 'Action.GetMeal':
            # 날짜 엔티티 공백인 경우 현재날짜로 값 넣기
            if df_result['queryResult']['parameters']['date-time'] == '':
                d = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
                df_result['queryResult']['parameters']['date-time'] = d.strftime('%Y-%m-%d') + 'T12:00:00+09:00'

            entities = df_result['queryResult']['parameters']
            if entities['MealTime'] == '조식':
                mealtime = 1
            elif entities['MealTime'] == '석식':
                mealtime = 3
            else:
                mealtime = 2

            if (entities['SchoolName'] != '') or (user.last_school_code != ''):
                if entities['SchoolName'] != '':  # 학교명을 직접 지정한 경우
                    try:
                        school_list = self.neis.search_school(entities['SchoolName'])
                    except Exception as e:
                        self.fm.send(
                            user.uid,
                            '학교 조회 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.\n'
                            '문제가 지속될 경우, 아래 \'버그 신고하기\'를 이용해서 신고해 주세요.',
                            Templates.QuickReplies.after_system_error
                        )

                        self.logger.log(
                            '나이스 학교 조회중 오류 발생!',
                            'ERROR',
                            'RECIPIENT: {0}, DETAILS: {1}'.format(user.uid, str(e))
                        )

                        return

                    if len(school_list) == 0:  # 일치하는 학교가 없는 경우
                        self.fm.send(
                            user.uid,
                            '학교 \'{0}\'를 찾을 수 없어요.'.format(entities['SchoolName']),
                            Templates.QuickReplies.after_user_error
                        )
                        return

                    elif len(school_list) > 1:  # 나이스에서 2개 이상의 학교를 찾음
                        # 안내 메시지 보내기
                        self.fm.send(user.uid, '여러 학교가 검색되었어요. 원하는 학교의 버튼을 선택해 주세요.')
                        self.fm.typing(user.uid)

                        [_, month, day] = entities["date-time"].split('T')[0].split['-']

                        # 카드 만들어서 붙이기
                        school_cards = []
                        for sch in school_list:
                            school_cards.append({
                                'title': sch.name + ' (%s)' % sch.region_hangul,
                                'image_url': '',
                                'subtitle': sch.address,
                                "buttons": [
                                    {
                                        "type": "postback",
                                        "title": '{0}월 {1}일 {2} ({3}) 의 급식 보기'.format(
                                            month, day, sch.name, sch.region_hangul
                                        ),
                                        "payload": 'M_{0}_{1}_{2}'.format(
                                            sch.code,
                                            entities["date-time"].split('T')[0],
                                            str(mealtime)
                                        )
                                    }
                                ]
                            })

                        # 유저한테 보내기
                        card = Elements.Card(school_cards)
                        self.fm.send(user.uid, card)
                        return

                    else:  # 힉교가 정상적으로 하나만 나옴
                        sch = school_list[0]
                        self.process_postback(
                            user,
                            'M_{0}_{1}_{2}'.format(
                                sch.code,
                                entities["date-time"].split('T')[0],
                                str(mealtime)
                            )
                        )
                else:  # 학교명을 생략한 경우 -> 디비에 저장된 마지막 요청 학교를 가져온다.
                    self.process_postback(
                        user,
                        'M_{0}_{1}_{2}'.format(
                            user.last_school_code,
                            entities["date-time"].split('T')[0],
                            str(mealtime)
                        )
                    )

            else:  # 학교 이름을 지정하지도 않았고 전에 사용한 기록도 없음.
                # 에러 / Abort
                self.fm.send(
                    user.uid,
                    '이전에 요청한 학교가 없습니다. 처음 요청 시에는 학교 이름을 포함해서 요청해 주세요.',
                    Templates.QuickReplies.after_user_error
                )
                return

        else:  # Unknown Entity
            self.fm.send(user.uid, '무슨 뜻인지 잘 모르겠어요.', Templates.QuickReplies.after_user_error)
            return

        return

    def process_postback(self, user, payload):
        self.fm.typing(user.uid)

        # 페이로드 분기
        if payload == 'FACEBOOK_WELCOME':
            # 01
            self.fm.send(user.uid, '안녕하세요! 만나서 반가워요🤗')
            # 02
            self.fm.send(user.uid, '저는 급식봇이라고 해요.')

            self.fm.send(
                user.uid,
                '제 안에 있는 인공지능 덕분에 저는 다양한 말을 알아들을 수 있어요😎\n'
                '이제 제가 할 수 있는 일을 알아볼까요?',
                Templates.QuickReplies.intro
            )

            return

        elif payload == 'INTRO_MORE':
            # 1/1 (Card)
            card = Elements.Card(Templates.Cards.intro_features)
            self.fm.send(user.uid, card)

            return

        # 사용법
        elif payload == 'HELP':
            # 1/3 (Text)
            msg_str = '다양한 방법으로 급식을 가져올 수 있어요!\n' \
                      '예시:' \
                      '> 급식고등학교 내일 저녁\n' \
                      '> 3월 14일 급식고등학교 급식\n' \
                      '> 급식고등학교\n' \
                      '> 내일은?\n' \
                      '기본값은 오늘 날짜의 중식이에요.'
            self.fm.send(user.uid, msg_str)

            # 2/3 (Text)
            msg_str = '학교 이름을 생략한 경우, 바로 전에 요청하셨던 학교의 급식을 자동으로 가져올 거에요.\n' \
                      '예시:\n' \
                      '12:00 > 오늘 다솜중 급식이 뭐야?\n' \
                      '12:01 > 내일은?\n' \
                      '그렇기 때문에, 위의 경우에는 다솜중학교의 \'내일\' 급식을 가져옵니다.'
            self.fm.send(user.uid, msg_str)

            # 3/3 (Text)
            self.fm.send(user.uid, '혹시라도 잘 이해가 가지 않으시면 그냥 학교 이름을 입력해 보세요.')

            return

        # 급식 급식 급식!
        elif payload.startswith('M_'):
            [_, school_code, tmp_date, mealtime] = payload.split('_')
            user.last_school_code = school_code

            # 급식 가져오기
            sch = self.neis.school_from_code(school_code)
            date = datetime.datetime.strptime(tmp_date, "%Y-%m-%d")
            meal = sch.get_meal(date, int(mealtime))  # Menu 객체의 배열

            if int(mealtime) == 1:
                mt_text = '아침'
            elif int(mealtime) == 3:
                mt_text = '저녁'
            else:
                mt_text = '점심'

            # 잘 포장해서 보낸다
            if len(meal) != 0:  # 급식이 존재할 때
                meal_text = ''
                for menu in meal:
                    meal_text = '{0}{1} {2}'.format(meal_text, menu.name, menu.allergy)
                meal_text = meal_text.rstrip()

                self.fm.send(
                    user.uid,
                    '%d년 %d월 %d일 %s의 %s 메뉴에요! 😀\n%s'
                    % (
                        int(date.year),
                        int(date.month),
                        int(date.day),
                        sch.name,
                        mt_text,
                        meal_text
                    ),
                    Templates.QuickReplies.after_meal
                )

            else:  # 밥없음
                self.fm.send(
                    user.uid,
                    '%d년 %d월 %d일 %s의 %s 메뉴가 없어요ㅜㅜ\n(또는 나이스에 등록이 안된 것일수도 있어요)'
                    % (
                        int(date.year),
                        int(date.month),
                        int(date.day),
                        sch.name,
                        mt_text
                    ),
                    Templates.QuickReplies.after_meal
                )

            return

        elif payload == 'BUG_REPORT':
            self.fm.send(user.uid, '아래 버튼을 눌러서 신고해주세요.')

            tmp_c = Templates.Cards.bug_report
            tmp_c[0]['buttons'][0]['url'] += user.uid
            card = Elements.Card(tmp_c)
            self.fm.send(user.uid, card, Templates.QuickReplies.after_action)

            return

        elif payload == 'ATTACHMENTS':
            self.fm.send(user.uid, ':)', Templates.QuickReplies.after_action)
