import datetime
from logger import Logger
from user import User


class FireStore:
    def __init__(self, config):
        self.config = config
        self.logger = Logger()

        self.logger.log("FS class was initialized.")

        return

    def get_user(self, uid):
        """
        Search user from firestore db, return the user object.
        :param uid: Facebook Messenger recipient_id
        :return: User Object (없으면 None)
        """

        """
        여기서
        지지고
        볶고
        하세요
        """

        # 유저 조회가 실패하면 None 리턴

        user_config = {
            "uid": uid,
            "new_user": False,
            "user_details": {
                "name": None,    # 있으면 가져오기
                "use_count": 0,   # TODO
                "register_date": datetime.datetime.now()    # TODO
            }
        }

        r_user = User(user_config, self.config)

        return r_user

