import requests
import json
from logger import Logger


# 메시지 요소 (카드, 빠른 답장 등 클래스)
class MessageElements:
    def __init__(self):
        pass

    class Card:
        def __init__(self, payload):
            self.payload = payload

    class QuickReply:
        def __init__(self, payload):
            self.payload = payload


class FacebookMessenger:
    def __init__(self, config):
        self.endpoint = "https://graph.facebook.com/v3.3/me/messages?access_token="
        self.config = config

        return

    def typing(self, uid):
        # 바디 / 헤더
        headers = {'content-type': 'application/json'}
        body = {"recipient": {"id": uid}, "sender_action": "typing_on"}

        # 보낸다
        requests.post(
            self.endpoint + self.config['FACEBOOK']['ACCESS_TOKEN'],
            data=json.dumps(body),
            headers=headers
        )

        return

    def send(self, recipient, thing, qr=None):
        # Detect type of 'thing' and Send it accordingly
        pass

        # 기본 헤더 / 바디
        headers = {'content-type': 'application/json'}
        body = {
            "recipient": {
                "id": recipient
            },
            "message": {}
        }

        # 단순 문자열일 때
        if isinstance(thing, str):
            body['message']['text'] = thing

        # 카드일 때
        elif isinstance(thing, MessageElements.Card):
            body['message']['attachment'] = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": []
                }
            }

            for card in thing.payload:
                for item in card:
                    card[item] = card[item].replace('%rootdir%', self.config['SITE']['ROOT_URL'])
                body['message']['attachment']['payload']['elements'].append(card)

        # 빠른 답장 추가하기
        if isinstance(qr, MessageElements.QuickReply):
            for i in qr.payload:
                body['message']['quick_replies'] = []
                body['message']['quick_replies'].append(i)
        elif type(MessageElements) == dict:
            for i in qr:
                body['message']['quick_replies'] = []
                body['message']['quick_replies'].append(i)

        # 보낸다
        requests.post(
            self.endpoint + self.config['FACEBOOK']['ACCESS_TOKEN'],
            data=json.dumps(body),
            headers=headers
        )

        return


# 기타 그래프 API 잡일들을 처리하는 클래스
class Graph:
    def __init__(self, config):
        self.config = config
        self.logger = Logger()
        pass

    def get_name(self, uid):
        """

        :param uid: Recipient_ID
        :return: str, 실패하면 유저N
        """
        # 페이스북 Graph Api 를 사용해 사용자의 진짜 이름을 가져옵니다.
        url = 'https://graph.facebook.com/%s?fields=first_name,last_name&access_token=%s' \
              % (uid, self.config['FACEBOOK']['ACCESS_TOKEN'])

        response = requests.get(url)
        response_body = response.json()

        try:
            if response.status_code == 200:
                # response_body['last_name']
                return response_body['first_name'] + response_body['last_name']
            else:
                self.logger.log("그래프 > get_name 에서 Graph 응답이 200이 아닙니다!", "ERROR", "RECIPIENT: {0}".format(uid))
                return '유저{0}'.format(uid)
        except KeyError as e:
            self.logger.log(
                "그래프 > get_name 에서 KeyError가 발생했습니다!",
                "ERROR", "RECIPIENT: {0}, Error: {1}".format(uid, str(e))
            )
            return '유저{0}'.format(uid)
