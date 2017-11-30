DEBUG = 0
INFO = 1
ERROR = 2


class Logger:

    LOG_LEVEL = 1

    def log(self, *args, **kwargs):
        level = kwargs.pop('level', INFO)
        if level >= self.LOG_LEVEL:
            print(*args, **kwargs)

logger = Logger()
log = logger.log

if __name__ == '__main__':
    Logger.LOG_LEVEL = 1
    log(1, 2, 3, sep='\t', level=DEBUG)
    log(4, 5, 6, sep='\t\t', level=INFO)
