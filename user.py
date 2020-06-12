import json
import requests

from message import MessageElements


class User:
    # 초기화 메서드
    def __init__(self, req, config):
        # 디비에서 불러온는 경우는



        # config
        self.config = config
        self.graph_endpoint = "https://graph.facebook.com/v3.3/me/messages?access_token="

        # 페북 관련
        self.uid = req['sender']['id']
        self.name = None

        return

    # 페이스북 Graph Api 를 사용해 사용자의 진짜 이름을 가져옵니다.
    def get_name(self):
        # 이미 이름을 가져왔거나 또는 고스트일 때
        if self.name or self.is_ghost:
            pass
        else:
            url = 'https://graph.facebook.com/%s?fields=first_name,last_name&access_token=%s' \
                  % (self.uid, self.config['FACEBOOK']['ACCESS_TOKEN'])

            response = requests.get(url)
            response_body = response.json()

            try:
                if response.status_code == 200:
                    self.name = (response_body['first_name'], response_body['last_name'])
                    return
                else:
                    return
            except KeyError:
                return

    def send(self, target, qr=None):
        # Detect type of 'something' and Send it accordingly
        pass

        # 기본 헤더 / 바디
        headers = {'content-type': 'application/json'}
        body = {
            "recipient": {
                "id": self.uid
            },
            "message": {}
        }

        # 단순 문자열일 때
        if isinstance(target, str):
            body['message']['text'] = target

        # 카드일 때
        elif isinstance(target, MessageElements.Card):
            body['message']['attachment'] = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": []
                }
            }

            for card in target.payload:
                body['message']['attachment']['payload']['elements'].append(card)

        # 빠른 답장 추가하기
        if isinstance(qr, MessageElements.QuickReply):
            for i in qr.payload:
                body['message']['quick_replies'] = []
                body['message']['quick_replies'].append(i)

        # 보낸다
        requests.post(
            self.graph_endpoint + self.config['FACEBOOK']['ACCESS_TOKEN'],
            data=json.dumps(body),
            headers=headers
        )

        return

    # 메신저에서 '타이핑' 하고 있는 것처럼 보이게 하기
    def typing(self):
        # 바디 / 헤더
        headers = {'content-type': 'application/json'}
        body = {"recipient": {"id": self.uid}, "sender_action": "typing_on"}

        # 보낸다
        requests.post(
            self.graph_endpoint + self.config['FACEBOOK']['ACCESS_TOKEN'],
            data=json.dumps(body),
            headers=headers
        )

        return


