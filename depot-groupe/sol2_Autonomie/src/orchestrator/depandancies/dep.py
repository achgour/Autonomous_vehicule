# ---------------------------------------------------------------------------- #
#                                    Logging                                   #
# ---------------------------------------------------------------------------- #
import logging

class ColoredFormatter(logging.Formatter):
    """Logging Formatter to add pretty colors and formatting"""
    green = "\x1b[32m"
    red = "\x1b[91m"
    grey = "\x1b[37m"
    yellow = "\x1b[33m"
    bold_red = "\x1b[31m"
    reset = "\x1b[0m"
    format = "%(name)s %(message)s (%(filename)s:%(lineno)d)"

    singleton = None

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    
class DLogger:
    """Class used to setup the logging system"""
    def setup_logger(name: str) -> logging.Logger:
        """Should be called instead of the first call to logging.getLogger(name)"""
        ch = logging.StreamHandler()
        ch.setFormatter(ColoredFormatter.singleton)

        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)
        log.addHandler(ch)
        return log

    def setup_loggers():
        """Removes the default handler of the root logger.
        It prevents double logging
        """
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().removeHandler(logging.getLogger().handlers[0])
        ColoredFormatter.singleton = ColoredFormatter()

# ---------------------------------------------------------------------------- #
#                           Socket classes definition                          #
# ---------------------------------------------------------------------------- #
import socket
import os

class DSocket:
    """Mother class implementing functions relative to Unix Socket    """
    def __init__(self,socket_path:str, logger:str):
        """Initialize Socket
        
        Args:
            socket_path (str): File path to the unix socket
            logger (str): Name of the logger to log to
        """
        self.logger = DLogger.setup_logger(logger)
        self.Socket = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        self.Socket.connect(socket_path)
        self.connection:socket.socket = None
        # This flag is used to stop the listening thread
        self.should_stop = False
        while not (os.path.exists(socket_path)):
            pass  # While the socket server doesn't exist
        self.logger.info("Connected to UNIX Socket")
        self.should_stop = False
        
    def listen(self):
        pass
    
    def send(self, response: str):
        pass

    def stop(self):
        self.should_stop = True
        # We need to close the connection to avoid a deadlock
        if self.connection:
            self.connection.close()
    
    