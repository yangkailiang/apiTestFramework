from logging import  DEBUG, INFO, WARNING, ERROR, CRITICAL, getLogger, Formatter, Handler
from Common.utils import SingletonMeta


class CustomFormatter(Formatter):
    def format(self, record):
        record.message = f"{f'{record.identification} - ' if hasattr(record, 'identification') else ''}" + record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s


class ResultHandler(Handler):
    def __init__(self, result):
        super(ResultHandler, self).__init__()
        self.result = result
        self.setFormatter(CustomFormatter('%(levelname)s - %(asctime)s - %(filename)s[line:%(lineno)d] - %(message)s'))

    def emit(self, record):
        message = self.format(record)
        self.result.append(message)


class Logger(metaclass=SingletonMeta):
    level_relations = {
        'debug': DEBUG,
        'info': INFO,
        'warning': WARNING,
        'error': ERROR,
        'crit': CRITICAL
    }

    def __init__(self):
        # pass
        # filename = LOG_DIR + '/sys.log'
        self.logger = getLogger("SYS")
        self.logger.setLevel(self.level_relations.get('info'))
        # 设置日志格式
        self.format_str = CustomFormatter('%(levelname)s - %(asctime)s - %(filename)s[line:%(lineno)d] - %(message)s')
        # if LOG_OUTPUT_CONSOLE:
        #     # 往屏幕上输出
        #     sh = StreamHandler()
        #     # # 设置屏幕上显示的格式
        #     sh.setFormatter(format_str)
        #     self.logger.addHandler(sh)
        #
        # # 往文件里写入#指定间隔时间自动生成文件的处理器
        # th = handlers.RotatingFileHandler(
        #     filename, maxBytes=5e6, backupCount=10, encoding="utf-8"
        # )
        # # 设置文件里写入的格式
        # th.setFormatter(format_str)
        # # 把对象加到logger里
        # self.logger.addHandler(th)


__all__ = ['Logger', "ResultHandler"]

if __name__ == '__main__':
    pass
