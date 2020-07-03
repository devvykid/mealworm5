import datetime

from logger import Logger
from user import User

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FireStoreController:
    def __init__(self, config):
        self.config = config
        self.logger = Logger()
        self.logger.log("FS was initialized.")

        # Use the application default credentials
        self.cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(self.cred, {
            'projectId': config['GOOGLE']['PROJECT_ID'],
        })

        self.db = firestore.client()

        return

    def get_user(self, uid):
        """
        Search user from firestore db, return the user object.
        :param uid: User ID (Recipient ID)
        :return: User Object (없으면 None)
        """

        doc_ref = self.db.collection('users').document(uid)
        try:
            doc = doc_ref.get()
            doc_dict = doc.to_dict()

        except Exception as e:
            self.logger.log('FS: 유저 조회 실패: {0}'.format(uid), 'ERROR', str(e))
            return None

        user_config = {
            "uid": uid,
            "new_user": False,
            "user_details": {
                "name": doc_dict['name'],
                "use_count": doc_dict['use_count'],
                "since": datetime.datetime.strptime(doc_dict['since'], '%Y-%m-%d-%H-%M-%S')
            },
            "last_school_code": doc_dict['last_school_code']
        }

        r_user = User(user_config, self.config)

        return r_user

    def save_user(self, user):
        doc_ref = self.db.collection('users').document(user.uid)
        doc_ref.set({
            'name': user.name,
            'use_count': user.use_count,
            'since': datetime.datetime.strftime(user.since, '%Y-%m-%d-%H-%M-%S'),
            'last_school_code': user.last_school_code
        })

    def update_user(self, user, key, value):
        doc_ref = self.db.collection('users').document(user.uid)
        doc_ref.set({
            key: value
        })
