from user import User
from message import Message
from nlp import LuisController, DateProcessing
from logger import Logger


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
            m = '처음 만나서 반가워요! 저는 앞으로 당신의 학교생활을 책임질 급식봇이에요 😇'
            user.send_message(m)

            # 디비에 등록
            user.register()

            return
