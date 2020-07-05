import requests
import json


class DialogFlowController:
    def __init__(self, g_config):
        # Endpoint Config
        self.endpoint = 'https://dialogflow.googleapis.com'

        # Read API Keys from config
        self.project_id = g_config['DIALOGFLOW']['DIALOGFLOW_PROJECT_ID']
        self.access_token = g_config['DIALOGFLOW']['DIALOGFLOW_ACCESS_TOKEN']

        return

    def analyze(self, query, user_id, session):
        req_url = '/v2/projects/%s/agent/environments/-/users/%s/sessions/%s:detectIntent' \
                  % (self.project_id, user_id, session)

        querystring = {
            'access_token': self.access_token
        }

        payload = json.dumps({
            'queryInput': {
                'text': {
                    'text': query,
                    'languageCode': 'ko'
                }
            },
            'queryParams': {
                'timeZone': 'Asia/Seoul'
            }
        })

        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

        response = requests.request('POST', self.endpoint + req_url, data=payload, headers=headers, params=querystring)

        result = response.json()

        '''
        [Sample Response Body]
        {
            'responseId': '[REDACTED]',
            'queryResult': {
                'queryText': 'ㅎㅇㅎㅇ',
                'action': 'input.welcome',
                'parameters': {},
                'allRequiredParamsPresent': true,
                'fulfillmentText': '안녕하세요!',
                'fulfillmentMessages': [
                    {
                        'text': {
                            'text': [
                                '안녕하세요!'
                            ]
                        }
                    }
                ],
                'intent': {
                    'name': '[REDACTED]',
                    'displayName': 'Communication.Hi'
                },
                'intentDetectionConfidence': 1,
                'languageCode': 'ko'
            }
        }
        
        {
          'responseId': 'fca3653c-215e-4f79-aec5-b977f0ae0eeb-425db6e2',
          'queryResult': {
            'queryText': '내일 진관중 급식',
            'parameters': {
              'date-time': '2020-07-04T12:00:00+09:00', # 선택적(공백)
              'SchoolName': '진관중',  # 선택적(공백)
              'MealTime': '중식'  # Mealtime 밸류는 반드시 존재
            },
            'allRequiredParamsPresent': true,
            'fulfillmentMessages': [
              {
                'text': {
                  'text': [
                    ''
                  ]
                }
              }
            ],
            'intent': {
              'name': 'projects/mealworm5/agent/intents/caba7e69-960e-47d1-bc17-254b0d9a1514',
              'displayName': 'Action.GetMeal'
            },
            'intentDetectionConfidence': 1,
            'languageCode': 'ko'
          }
        }
        
        '''
        from app.log import Logger
        if result.get('error'):
            raise ValueError(response.text)

        Logger.log('Dialogflow API 처리 완료!', 'NOTICE', '요청 query: %s' % query)

        return {
            'intent': result['queryResult']['intent']['displayName'],
            'isfallback': result['queryResult']['intent'].get('isFallback', False),
            'confidence': result['queryResult']['intentDetectionConfidence'],
            'reply': result['queryResult'].get('fulfillmentText', None)
        }
