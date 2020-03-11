import requests
import datetime
import pytz
import configparser


class LuisController:
    def __init__(self):
        # Init
        self.result = None

        # read config
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.LUIS_ENDPOINT = config['LUIS_APP_URI'] + config['LUIS_APP_ID']

        self.LUIS_HEADERS = {
            'Ocp-Apim-Subscription-Key': config['LUIS_KEY']
        }

        self.LUIS_PARAMS = {
            'timezoneOffset': '540',  # 60 x 9 -> UTC+9 (Asia/Seoul)
            'verbose': 'false',
            'spellCheck': 'false',
            'staging': 'false',
        }

        pass

    def get_analysis_results(self, string):
        self.LUIS_PARAMS['q'] = string

        r = requests.get(
            self.LUIS_ENDPOINT,
            headers=self.LUIS_HEADERS,
            params=self.LUIS_PARAMS
        )
        self.result = r.json()

        return r.json()


class DateProcessing:
    def __init__(self):
        pass

    @staticmethod
    def parse_date(entities):
        pass

