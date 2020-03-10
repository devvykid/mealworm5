class Message:
    def __init__(self, msg_type, msg_data, quick_replies=None):
        self.type = msg_type
        self.data = msg_data
        self.qr = quick_replies

        return
