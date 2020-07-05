import logging


class Logger:
    def __init__(self):
        return

    @staticmethod
    def log(payload, level='NOTICE', details=''):
        # Three log levels: NOTICE, WARN, ERROR
        # TODO: Timestamp
        # TODO: Make It Async
        try:
            if level == 'ERROR':
                logging.error(payload + details)
            elif level == 'WARN':
                logging.warning(payload + details)
            elif level == 'NOTICE':
                logging.info(payload + details)
        except Exception as e:
            logging.error('[Logger > log] 로깅 중 오류가 발생하였습니다: {0}'.format(e))

        # TODO: Implement Send Mail (GAE)

        return

    def bugreport(self, uid, title, details, contact):
        # TODO
        return
