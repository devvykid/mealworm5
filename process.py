from user import User
from message import Message
from nlp import LuisController, DateProcessing
from logger import Logger
from template import Templates


class Processing:
    def __init__(self):
        self.logger = Logger()
        pass

    def process_message(self, user, message):
        user.typing()

        # 1. LUIS 콜
        luis = LuisController()
        try:
            luis.get_analysis_results(message)
            intent = luis.result['topScoringIntent']['intent']
        except KeyError:
            self.logger.log('Luis.ai API 오류!', 'ERROR')
            em = Message('TEXT', '죄송합니다, 급식봇에 오류가 발생했습니다.\n'
                                 '자세한 정보: 자연어 분석에 실패했습니다.\n'
                                 '다시 시도해 주시고 오류가 계속되면 아래의 \'버그 신고하기\' 기능을 이용해 주세요.')
            user.send_message(em)
            return
        except Exception as e:
            self.logger.log('Luis.ai 기타 오류!: %s' % str(e), 'ERROR')
            em = Message('TEXT', '죄송합니다, 급식봇에 오류가 발생했습니다.\n'
                                 '자세한 정보: 자연어 분석에 알 수 없는 이유로 실패했습니다.\n'
                                 '다시 시도해 주시고 오류가 계속되면 아래의 \'버그 신고하기\' 기능을 이용해 주세요.')
            user.send_message(em)
            return

        # 2. Intent 분기
            # Intent: 소스 코드 보기
        if intent == 'Action.SourceCode':
            return

        # Intent: No
        elif intent == 'Communication.Etc.Swear':
            message = ':('

        # Intent: Yes
        elif intent == 'Communication.Paralang.Yes':
            message = ':)'

        # Intent: 부르기
        elif intent == 'Communication.Simple.Call':
            message = '네, 여기 있어요.'

        # Intent: 굿
        elif intent == 'Communication.Simple.Good':
            message = '고마워요!'

        # Intent: 개발자 정보
        elif intent == 'Communication.Who':

            return

        # Intent: 반가움
        elif intent == 'Communication.NiceToSeeYou':

            return

        # Intent: Yuck
        elif intent == 'Communication.Simple.Yuck':

            return

        # Intent: 버그 신고하기
        elif intent == 'Action.Report':
            fb.send_text_message(recipient_id, '아래 버튼을 눌러서 신고해주세요!')
            fb.send_cards(recipient_id, [
                {
                    "title": "버그 신고하기",
                    "image_url": "https://mw.api.oror.kr/static/siren.png",
                    "subtitle": "아래 버튼을 클릭하면 버그 신고 양식으로 연결됩니다. 감사합니다.",
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://mw.api.oror.kr/support/bugreport?id=%s" % recipient_id,
                            "title": "버그 잡으러 가기"
                        }
                    ]
                }
            ], 'DEFAULT')

            return

        # Intent: 도움말
        elif intent == 'Communication.Request.Help':
            return

        # Intent: 인사하기
        elif intent == 'Communication.Simple.Hi':
            pass
        # Intent: 급식
        elif intent == 'Communication.Request.Meal':
            pass

        else:
            pass



        return

    def process_postback(self, user, payload):
        user.typing()

        # 페이로드 분기
        if payload == 'FACEBOOK_WELCOME':  # <시작하기> 경우
            # 01
            user.get_name()
            if user.name: m = Message('TEXT', '안녕하세요, %s%s 님!' % (user.name[0], user.name[1]))
            else:         m = Message('TEXT', '안녕하세요!')
            user.send_message(m)

            # 02
            m = Message('TEXT', '처음 만나서 반가워요! 저는 앞으로 당신의 학교생활을 책임질 급식봇이에요 😇')
            user.send_message(m)

            # 03
            m = Message('TEXT',
                        '저는 인공지능 기술로 만들어져서, 다양한 말을 알아들을 수 있어요.\n'
                        '이제 제가 할 수 있는 일을 알아볼까요?',
                        quick_replies=Templates.QuickReplies.intro)
            user.send_message(m)

            # 디비에 등록
            user.register()

            return

        elif payload == 'INTRO_MORE':
            # 기능에 대해 더 알려준다
            pass

        elif payload == 'HELP_MEAL':
            # 사용법을 알려준다
            msg_str = '이렇게 사용하시면 돼요!\n' \
                      '예) 서울과고 내일 저녁 알려줄래?\n' \
                      '예) 3월 14일 한울중학교 급식 알려줘라\n' \
                      '예) 가람초등학교 급식\n' \
                      '(날짜를 생략한 경우 기본값으로 오늘 급식을 가져옵니다.)'
            m = Message('TEXT', msg_str)
            user.send_message(m)

            msg_str = '학교 이름을 생략하신 경우, 바로 전에 요청하셨던 학교의 급식을 자동으로 가져옵니다.\n' \
                      '예)\n' \
                      '12:00 > 오늘 다솜중 급식이 뭐야?\n' \
                      '12:01 > 내일은?\n' \
                      '이런 경우에는 다솜중학교의 \'내일\' 급식을 가져옵니다.'
            m = Message('TEXT', msg_str)
            user.send_message(m)

            m = Message('TEXT', '저는 인공지능으로 유저님의 말을 이해하기 때문에 이거하고 조금 다르게 말하셔도 돼요. 편하게 말해주세요🤗')
            user.send_message(m)

            return


