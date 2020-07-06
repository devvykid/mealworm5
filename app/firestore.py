import datetime

from app.user import User

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'mealworm5',
})

db = firestore.client()


class FireStoreController:
    def __init__(self):
        return

    @staticmethod
    def get_user(uid, g_config):
        """
        Search user from firestore db, return the user object.
        :param g_config: 글로벌 콘피그 파일
        :param uid: User ID (Recipient ID)
        :return: User Object (없으면 None)
        """

        doc_ref = db.collection('users').document(uid)
        try:
            doc = doc_ref.get()
            doc_dict = doc.to_dict()

            user_config = {
                'uid': uid,
                'new_user': False,
                'user_details': {
                    'name': doc_dict['name'],
                    'use_count': doc_dict['use_count'],
                    'since': datetime.datetime.strptime(doc_dict['since'], '%Y-%m-%d-%H-%M-%S')
                },
                'last_school_code': doc_dict['last_school_code']
            }

            return User(user_config, g_config)

        except Exception as e:
            from app.log import Logger
            Logger.log('[FS > get_user] 유저 조회 실패. (LIKELY 신규 유저) UID: {0}'.format(uid), 'WARN', str(e))
            return None

    @staticmethod
    def save_user(user):
        try:
            doc_ref = db.collection('users').document(user.uid)
            doc_ref.set({
                'name': user.name,
                'use_count': user.use_count,
                'since': user.since.strftime('%Y-%m-%d-%H-%M-%S'),
                'last_school_code': user.last_school_code
            })
        except Exception as e:
            from app.log import Logger
            Logger.log('[FS > save_user] 유저 저장 실패. UID: {0}'.format(user.uid), 'ERROR', str(e))
            return None

        return True

    @staticmethod
    def save_meal(user, meal):
        try:
            doc_ref = db.collection('meal').document(meal['meal_id'])
            doc_ref.set(meal)
        except Exception as e:
            from app.log import Logger
            Logger.log('[FS > save_meal] 급식 저장 실패. UID: {0}'.format(user.uid), 'ERROR', str(e))
            return None

        return True
        pass

    @staticmethod
    def get_meal(school_code, date, mealtime):
        doc_ref = db.collection('meal')\
            .where('school_code', '==', school_code)\
            .where('date', '==', date)\
            .where('mealtime', '==', int(mealtime))

        try:
            doc = doc_ref.get()
            doc_dict = doc.to_dict()

            print(doc_dict)

            return doc_dict

        except Exception as e:
            from app.log import Logger
            Logger.log('[FS > get_user] 급식이 DB에 없습니다.', 'INFO', str(e))
            return None
