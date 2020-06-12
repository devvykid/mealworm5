import requests
import json
from logger import Logger


class DialogFlow:
    def __init__(self, config):
        # Endpoint Config
        self.endpoint = "https://dialogflow.googleapis.com"

        # Read API Keys from config.ini
        self.project_id = config['DIALOGFLOW']['DIALOGFLOW_PROJECT_ID']
        self.access_token = config['DIALOGFLOW']['DIALOGFLOW_ACCESS_TOKEN']

        self.logger = Logger()

        return

    def analyze(self, query, user_id, session):
        req_url = '/v2/projects/%s/agent/environments/-/users/%s/sessions/%s:detectIntent' \
                  % (self.project_id, user_id, session)

        querystring = {
            "access_token": self.access_token
        }

        payload = json.dumps({
            "queryInput": {
                "text": {
                    "text": query,
                    "languageCode": "ko"
                }
            },
            "queryParams": {
                "timeZone": "Asia/Seoul"
            }
        })

        headers = {
            'accept': "application/json",
            'content-type': "application/json"
        }

        response = requests.request("POST", self.endpoint + req_url, data=payload, headers=headers, params=querystring)

        result = response.json()

        """
        [Sample Response Body]
        {
            "responseId": "[REDACTED]",
            "queryResult": {
                "queryText": "ㅎㅇㅎㅇ",
                "action": "input.welcome",
                "parameters": {},
                "allRequiredParamsPresent": true,
                "fulfillmentText": "안녕하세요!",
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                "안녕하세요!"
                            ]
                        }
                    }
                ],
                "intent": {
                    "name": "[REDACTED]",
                    "displayName": "Communication.Hi"
                },
                "intentDetectionConfidence": 1,
                "languageCode": "ko"
            }
        }
        """
        if result.get('error'):
            self.logger.log('DialogFlow API에서 오류가 발생했습니다.', 'ERROR', response.text)
            return None

        self.logger.log('Dialogflow API 처리 완료!', 'NOTICE', '요청 query: %s' % query)

        return {
            'intent': result['queryResult']['intent']['displayName'],
            'isfallback': result['queryResult']['intent'].get('isFallback', False),
            'confidence': result['queryResult']['intentDetectionConfidence'],
            'reply': result['queryResult'].get('fulfillmentText', None)
        }

