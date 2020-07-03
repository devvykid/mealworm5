import datetime
import pytz
from facebook import Graph


class User:
    # 초기화 메서드
    def __init__(self, user_config, config):
        # config
        self.config = config
        self.fg = Graph(config)

        # 유저 콘피그를 들여다본다
        self.uid = user_config['uid']
        if user_config['new_user'] is True:  # 신규 유저로 app.py 에서 생성됨
            self.since = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
            self.use_count = 1
            self.name = self.fg.get_name(uid=self.uid)
            self.last_school_code = ""
        else:  # Firestore 에서 해동됨
            self.since = user_config['user_details']['since']
            self.use_count = user_config['user_details']['use_count'] + 1
            self.name = user_config['user_details']['name']
            self.last_school_code = user_config['last_school_code']
        return
