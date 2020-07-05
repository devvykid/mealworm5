import requests
import json


# 메시지 요소 (카드, 빠른 답장 등 클래스)
class MessageElements:
    def __init__(self):
        return

    class Card:
        def __init__(self, payload):
            self.payload = payload

    class QuickReply:
        def __init__(self, payload):
            self.payload = payload


class FacebookMessenger:
    def __init__(self, g_config):
        self.endpoint = 'https://graph.facebook.com/v3.3/me/messages?access_token='
        self.access_token = g_config['FACEBOOK']['ACCESS_TOKEN']

        self.site_root = g_config['SITE']['ROOT_URL']

        return

    def typing(self, uid):
        # 바디 / 헤더
        headers = {'content-type': 'application/json'}
        body = {'recipient': {'id': uid}, 'sender_action': 'typing_on'}

        # 보낸다
        requests.post(self.endpoint + self.access_token, data=json.dumps(body), headers=headers)

        return

    def send(self, recipient, thing, quick_replies=None):
        # 기본 헤더 / 바디
        headers = {'content-type': 'application/json'}
        body = {'recipient': {'id': recipient}, 'message': {}}

        # 단순 문자열일 때
        if isinstance(thing, str):
            body['message']['text'] = thing

        # 카드일 때
        elif isinstance(thing, MessageElements.Card):
            body['message']['attachment'] = {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': []
                }
            }

            for card in thing.payload:
                for key in card:
                    card[key] = card[key].replace('%rootdir%', self.site_root)
                body['message']['attachment']['payload']['elements'].append(card)

        # 빠른 답장 추가하기
        if isinstance(quick_replies, MessageElements.QuickReply):
            for qr in quick_replies.payload:
                body['message']['quick_replies'] = []
                body['message']['quick_replies'].append(qr)
        elif type(MessageElements) == dict:
            for qr in quick_replies:
                body['message']['quick_replies'] = []
                body['message']['quick_replies'].append(qr)

        requests.post(self.endpoint + self.access_token, data=json.dumps(body), headers=headers)

        return


# 기타 그래프 API 잡일들을 처리하는 클래스
class Graph:
    def __init__(self, g_config):
        self.config = g_config
        return

    def get_name(self, uid):
        """
        uid번 사용자의 이름을 Graph Api에서 가져온다.
        :param uid: Recipient_ID
        :return: str, 실패하면 유저N
        """
        # 페이스북 Graph Api 를 사용해 사용자의 진짜 이름을 가져옵니다.
        url = 'https://graph.facebook.com/%s?fields=first_name,last_name&access_token=%s' \
              % (uid, self.config['FACEBOOK']['ACCESS_TOKEN'])

        resp = requests.get(url)
        resp_json = resp.json()

        try:
            if resp.status_code == 200:
                return resp_json['first_name'] + resp_json['last_name']
            else:
                from app.log import Logger
                Logger.log('[Graph > get_name] API 응답 코드가 200이 아닙니다!', 'ERROR', 'RECIPIENT: {0}'.format(uid))
                return '유저{0}'.format(uid)
        except KeyError as e:
            from app.log import Logger
            Logger.log(
                '[Graph > get_name] API KeyError가 발생했습니다!',
                'ERROR',
                'RECIPIENT: {0}, Error: {1}'.format(uid, str(e))
            )
            return '유저{0}'.format(uid)
