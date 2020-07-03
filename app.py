"""
MEALWORM™ Server, version 5.

(c) 2018-2020 JY Park (devvykid).

For more information,
please refer to the link https://github.com/devvykid/mealworm5/ .
"""

from flask import Flask, request, render_template
import traceback
import configparser
import requests
import json

from process import Processing
from user import User
from firestore import FireStore
from facebook import FacebookMessenger
from logger import Logger

# 메타데이터
__author__ = "JeongYeon Park (devvykid)"
__ver__ = "20200605-rev1-fix0"

# 짜잔
app = Flask(__name__, static_url_path='/static')

# config.ini 읽어오기
g_config = configparser.ConfigParser()
g_config.read('config.ini')

# 객체 선언하기
ps = Processing(g_config)
fs = FireStore(g_config)
fm = FacebookMessenger(g_config)

logger = Logger()


@app.route('/')
def hello_world():
    # Make it Ra1n
    logger.log('Hello, world!', 'NOTICE', 'This is a test.')
    return '<code>make it ra1n</code>'


@app.route('/old', methods=['GET', 'POST'])
def old_deprecated():
    if request.method == 'GET':
        # Verification Test
        if request.args.get("hub.verify_token") == g_config['FACEBOOK']['OLD_VERIFY_TOKEN']:
            return request.args.get("hub.challenge")
        else:
            return 'Verification Failed!'

    if request.method == 'POST':
        try:
            req = request.get_json()

            for event in req['entry']:
                for e in event['messaging']:    # 요청의 단위 시작
                    if e.get('postback', {}).get('payload') or e.get('message'):
                        headers = {
                            'content-type': 'application/json'
                        }

                        body = {
                            "recipient": {
                                "id": e['sender']['id']
                            },
                            "message": {
                                "text": "이 버전의 급식봇은 서비스가 종료되었습니다. 새로운 급식봇5를 이용해 주세요!\n"
                                        "https://facebook.com/mealworm05/\n"
                                        "시작하기 전에 페이지 좋아요&팔로우는 필수! 아시죠?😎"
                            }
                        }

                        requests.post(
                            "https://graph.facebook.com/v3.3/me/messages?access_token=" +
                            g_config['FACEBOOK']['OLD_ACCESS_TOKEN'],
                            data=json.dumps(body),
                            headers=headers
                        )

        except Exception as e:
            print("Fuck: {}".format(str(e)))

        logger.log('Deprecated Request Processed.')
        return 'Deprecated Request Processed.'


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification Test
        if request.args.get("hub.verify_token") == g_config['FACEBOOK']['VERIFY_TOKEN']:
            return request.args.get("hub.challenge")
        else:
            return 'Verification Failed!'

    if request.method == 'POST':
        try:
            req = request.get_json()

            for event in req['entry']:
                for e in event['messaging']:    # 요청의 단위 시작
                    # 0-0. 고스트 확인
                    if req.get('message', {}).get('is_echo'):
                        continue

                    # 0-1. 디비에서 불러오기
                    user = fs.get_user(req['sender']['id'])

                    # 0-1-1. 신규 유저인 경우
                    if user is None:
                        logger.log("%s는 신규 유저입니다. 생성합니다..." % str(req['sender']['id']))
                        user_config = {
                            "new_user": True,
                            "uid": req['sender']['id']
                        }
                        user = User(user_config, g_config)

                    # 1-1. 포스트백 처리
                    if e.get('postback'):
                        if e['postback'].get('payload'):
                            ps.process_postback(user, e['postback']['payload'])
                        continue

                    # 1-2. 메시지 처리
                    elif e.get('message'):
                        # 1-2-1. 빠른 답장 포스트백 처리
                        if e['message'].get('quick_reply'):
                            if e['message']['quick_reply'].get('payload'):
                                ps.process_postback(user, e['message']['quick_reply']['payload'])
                                continue

                        # 1-2-2. 텍스트 메시지 처리
                        if e['message'].get('text'):
                            ps.process_message(user, e['message']['text'])
                            continue

                        # 1-2-3. 첨부파일 등이 있는 메시지
                        if e['message'].get('attachments'):
                            ps.process_postback(user, 'ATTACHMENTS')
                            continue

                    try:
                        fs.save_user(user)
                        logger.log(
                            '유저 세이브 완료: {0}'.format(user.uid),
                            'NOTICE'
                        )
                    except Exception as e:
                        logger.log(
                            'Firestore 유저 세이브 중 오류 발생: {0}'.format(str(e)),
                            'ERROR',
                            'RECIPIENT: {0}'.format(user.uid)
                        )

            return {"result", "fuck yeah!"}

        except Exception as e:
            traceback.print_exc()

            try:
                # 로거 (Lint 정상)
                logger.log("치명적 오류 발생!! RECIPIENT: {0}".format(req['sender']['id']), level="ERROR", details=str(e))

                fm.send(
                    req['sender']['id'],
                    '죄송합니다, 급식봇에 처리되지 않은 오류가 발생했습니다.\n'
                    '일시적인 오류인 경우, 다시 시도해 주세요. 계속적으로 오류가 발생하는 경우, '
                    '아래의 \'버그 신고하기\' 기능을 이용해 신고해 주세요.\n%s' % str(e)
                )

            except Exception:
                # 유언 못남김
                pass

            return {
                "result": "screwed"
            }


@app.route('/support/bugreport', methods=['GET', 'POST'])
def bugreport():
    if request.method == 'GET':
        u_id = request.args.get("id")
        if u_id:
            return render_template('bugreport.html', id=u_id)
        else:
            return render_template('bad.html', details='잘못된 접근이에요.')

    else:
        try:
            uid = request.form['id']
            title = request.form['title']
            details = request.form['steps_to_reproduce']

            contact = request.form.get('want_contact')
            if contact:
                contact = request.form['contact_information']

            if uid != request.args.get('id'):
                raise ValueError

            logger.bugreport(uid, title, details, contact)

            return render_template('success.html')

        except (KeyError, ValueError):
            return render_template('bad.html', details='잘못된 접근이에요.')

        except Exception as e:
            return render_template('bad.html', details='처리되지 않은 오류입니다: ' + str(e))


if __name__ == '__main__':
    app.run()
