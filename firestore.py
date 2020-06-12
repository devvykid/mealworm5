class FireStore:
    def __init__(self, config):
        pass

    def get_user(self, uid):
        """
        Search user from firestore db, return the user object.
        :param uid: Facebook Messenger recipient_id
        :return: User Object (없으면 None)
        """
