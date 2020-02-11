import configparser
import requests
import json


class User:
    def __init__(self, req):
        self.uid = req['sender']['id']

        self.is_ghost = 0
        self.name = None

        # check ghost
        if req.get('message'):
            if req['message'].get('is_echo'):
                self.is_ghost = 1

        # read config
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.FB_ACCESS_TOKEN = config['FACEBOOK']['ACCESS_TOKEN']
        self.GRAPH_URL = "https://graph.facebook.com/v3.3/me/messages?access_token="

        return

    def get_name(self):
        if self.name or self.is_ghost:
            pass
        else:
            request_url = 'https://graph.facebook.com/' + self.uid + \
                          '?fields=first_name,last_name' \
                          '&access_token=' + self.FB_ACCESS_TOKEN

            response = requests.get(request_url)
            result = response.json()

            if response.status_code == 200:
                self.name = (result['first_name'], result['last_name'])
                return
            else:
                return

    def get_data(self):
        pass

    def send_message(self, message):
        pass

    def typing(self):
        pass

    def register(self):
        pass