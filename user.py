import configparser
import requests
import json
import requests


class User:
    # 초기화 메서드
    def __init__(self, req):
        # 고스트 확인
        self.is_ghost = 0
        if req.get('message'):
            if req['message'].get('is_echo'):
                self.is_ghost = 1

        # 페북 관련
        self.uid = req['sender']['id']
        self.name = None

        # config.ini 읽어서 가져오기
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.FB_ACCESS_TOKEN = config['FACEBOOK']['ACCESS_TOKEN']
        self.GRAPH_URL = "https://graph.facebook.com/v3.3/me/messages?access_token="

        return

    # 페이스북 Graph Api 를 사용해 사용자의 진짜 이름을 가져옵니다.
    def get_name(self):
        # 이미 이름을 가져왔거나 또는 고스트일 때
        if self.name or self.is_ghost:
            pass
        else:
            url = 'https://graph.facebook.com/%s?fields=first_name,last_name&access_token=%s' \
                  % (self.uid, self.FB_ACCESS_TOKEN)

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

    # Message 객체를 유저에게 보냅니다.
    def send(self, msg):
        # 기본 헤더 / 바디
        headers = {'content-type': 'application/json'}
        body = {
            "recipient": {
                "id": self.uid
            },
            "message": {}
        }

        # 단순 문자열일 때
        if msg.type == 'TEXT':
            body['message']['text'] = msg.data

        # 카드일 때
        elif msg.type == 'CARD':
            body['message']['attachment'] = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": []
                }
            }

            for card in msg.data:
                body['message']['attachment']['payload']['elements'].append(card)

        # 빠른 답장 추가하기
        if msg.qr is not None:
            for i in msg.qr:
                body['message']['quick_replies'] = []
                body['message']['quick_replies'].append(i)

        # 보낸다
        requests.post(
            self.GRAPH_URL + self.FB_ACCESS_TOKEN,
            data=json.dumps(body),
            headers=headers
        )

        return

    # 메신저에서 '타이핑' 하고 있는 것처럼 보이게 하기
    def typing(self):
        # 바디 / 헤더
        headers = {'content-type': 'application/json'}
        body = {"recipient": {"id": self.uid}, "sender_action": "typing_on"        }

        # 보낸다
        requests.post(
            self.GRAPH_URL + self.FB_ACCESS_TOKEN,
            data=json.dumps(body),
            headers=headers
        )

        return

    # 디비에 유저 등록하기
    def register(self):
        pass

    # 마지막으로 성공한 학교 저장
    def save_school(self, school):
        # Parameter: school (School 객체)
        pass

    # 여러개 학교가 중복으로 떠서 리트시 전 학교를 기억하기 위한 함수
    def save_request(self, school_list, date, mealtime):
        # Parameters:
        # - 학교 리스트 (School 객체)
        # - 날짜 (Datetime 객체)
        # - Mealtime

        # 지난 DB 삭제

        # School 객체 Serialize (JSON -> TEXT)

        # 디비에 저장

        pass

    def get_request(self, code):
        # DB 조회

        # 코드 일치하는거 찾아서 De-Serialize

        # 리턴
        # 형식: (School 객체, date, mealtime)

        pass


