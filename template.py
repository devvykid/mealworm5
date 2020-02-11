import random


class Templates:
    class QuickReplies:
        after_action = [
            {
                "content_type": "text",
                'title': '굿!🎉',
                'payload': '',
                'image_url': ''
            },
            {
                "content_type": "text",
                'title': '📚도움말 보기',
                'payload': '',
                'image_url': ''
            },
            {
                "content_type": "text",
                'title': '🚨버그 신고하기',
                'payload': '',
                'image_url': ''
            },
            {
                "content_type": "text",
                'title': '💾소스 코드 보기',
                'payload': '',
                'image_url': ''
            }
        ]

        after_meal = [
            {
                'text': None,  # to be fulfilled
                'payload': '',
                'image_url': ''
            },
            {
                'text': '굿!🎉',
                'payload': '',
                'image_url': ''
            },
            {
                'text': '🚨버그 신고하기',
                'payload': '',
                'image_url': ''
            },
            {
                'text': '💾소스 코드 보기',
                'payload': '',
                'image_url': ''
            }
        ]

        default = [
            {
                'text': '오늘 급식',
                'payload': '',
                'image_url': ''
            },
            {
                'text': '내일 급식',
                'payload': '',
                'image_url': ''
            },
            {
                'text': '굿!🎉',
                'payload': '',
                'image_url': ''
            },
            {
                'text': '🚨버그 신고하기',
                'payload': '',
                'image_url': ''
            },
            {
                'text': '💾소스 코드 보기',
                'payload': '',
                'image_url': ''
            }
        ]

        intro = [
            {
                'text': '그래!😉',
                'payload': 'INTRO_MORE',
                'image_url': ''
            },
            {
                'text': '됬고, 사용법이나 알려줘.',
                'payload': 'HELP_MEAL',
                'image_url': ''
            }
        ]

    class Cards:
        intro_features = [
            {
                "title": "눈 깜짝할 새 급식 가져오기",
                "image_url": "https://mw.api.oror.kr/static/meal.jpg",
                "subtitle": "전국 초중고의 급식을 눈 깜짝할 새에 가져올 수 있어요. 앱 없이도요!",
                "buttons": [
                    {
                        "type": "postback",
                        "title": "어떻게 쓰는지 보기",
                        "payload": "HELP_MEAL"
                    }
                ]
            },
            {
                "title": "알러지 정보",
                "image_url": "https://mw.api.oror.kr/static/meal.jpg",
                "subtitle": "알러지가 있으셔도 걱정 마세요. 급식봇이 알아서 챙겨 줄 거에요.",
                "buttons": []
            },
            {
                "title": "[준비중] 급식 구독",
                "image_url": "https://mw.api.oror.kr/static/meal.jpg",
                "subtitle": "(준비중) 지정한 시간마다 매일 급식 알림을 받아보실 수 있어요.",
                "buttons": [
                    {
                        "type": "postback",
                        "title": "[🖖 곧 찾아옵니다!]",
                        "payload": ""
                    }
                ]
            }
        ]
