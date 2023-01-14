from loguru import logger


class AppException(Exception):
    """
    Represents a base application exception. Logs all exception messages
    if they are provided.
    """

    def __init__(self, msg: str = None, log_msg: str = None, *args):
        if msg or log_msg:
            logger.debug(log_msg or msg)
        super().__init__(msg, *args)
