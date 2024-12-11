import datetime
import logging
import sys


class ColoredFormatter(logging.Formatter):
    """Logging Formatter to add pretty colors and formatting"""
    green = "\x1b[32m"
    red = "\x1b[91m"
    grey = "\x1b[37m"
    yellow = "\x1b[33m"
    bold_red = "\x1b[31m"
    reset = "\x1b[0m"
    format_string = "%(name)s \t%(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format_string + reset,
        logging.INFO: green + format_string + reset,
        logging.WARNING: yellow + format_string + reset,
        logging.ERROR: red + format_string + reset,
        logging.CRITICAL: bold_red + format_string + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger(name: str) -> logging.Logger:
    """Should be called instead of the first call to logging.getLogger(name)"""
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    return log


def setup_loggers():
    """Setup both the std handler and the file handler
    """
    date = datetime.datetime.now()
    # Provides the date formatted as YYYYMMDD_HHMMSS
    logname = "log/"+str(date.strftime('%Y%m%d_%H%M%S'))+".log"
    format_string = "%(name).6s \t%(levelname).4s \t%(message)s (%(filename)s:%(lineno)d)"
    handler_std = logging.StreamHandler(sys.stdout)
    handler_std.setFormatter(ColoredFormatter())
    handler_file = logging.FileHandler(logname)
    handler_file.setFormatter(logging.Formatter(fmt=format_string))
    logging.basicConfig(encoding="utf-8", level=logging.DEBUG, handlers=[
                        handler_file, handler_std])