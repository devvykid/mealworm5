"""
MEALWORM™ Server, version 5.

(c) 2018-2020 JY Park. All rights reserved.

For more information,
please refer to the link https://github.com/computerpark/mealworm5 .

Thank you.
"""

from flask import Flask, request, jsonify, redirect, render_template
import traceback
import random
import configparser

from bug import Bug
from process import Processing
from user import User
from message import Message


app = Flask(__name__, static_url_path='/static')

config = configparser.ConfigParser()
config.read('config.ini')

ps = Processing()


@app.route('/')
def hello_world():
    return '<code>make it ra1n</code>'


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification Test
        if request.args.get("hub.verify_token") == config['FACEBOOK']['VERIFY_TOKEN']:
            return request.args.get("hub.challenge")
        else:
            return 'Verification Failed!'

    if request.method == 'POST':
        try:
            req = request.get_json()

            for event in req['entry']:
                for e in event['messaging']:    # 요청의 단위 시작
                    # 0-1. 생성
                    user = User(e)

                    # 0-2. 고스트 확인
                    if user.is_ghost == 1:
                        continue

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
                            m = Message('TEXT', ':)')
                            user.send_message(m)
                            continue

            return {"result", "fuck yeah!"}

        except Exception as e:
            traceback.print_exc()

            try:
                m = Message('TEXT', '죄송합니다, 급식봇에 처리되지 않은 오류가 발생했습니다.\n'
                                    '일시적인 오류인 경우, 다시 시도해 주세요. 계속적으로 오류가 발생하는 경우, '
                                    '아래의 \'버그 신고하기\' 기능을 이용해 신고해 주세요.\n%s' % str(e))
                user.send_message(m)

            except NameError:
                # 유언 못남김
                pass

            return {
                "result": "screwed",
                "holy_error_data": str(e)
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

            b = Bug(uid, title, details, contact)
            b.submit()

            return render_template('success.html')

        except (KeyError, ValueError):
            return render_template('bad.html', details='잘못된 접근이에요.')

        except Exception as e:
            return render_template('bad.html', details='처리되지 않은 오류입니다: ' + str(e))


if __name__ == '__main__':
    app.run()
