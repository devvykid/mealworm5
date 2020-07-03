import logging


class Logger:
    def __init__(self):
        pass

    def log(self, payload, level='NOTICE', details=''):
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
            logging.error('Error when logging: {0}'.format(e))

        # TODO: Implement Send Mail (GAE)

        return

    def bugreport(self, uid, title, details, contact):
        # TODO
        return
