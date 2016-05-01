import logging
import sys

logger = logging.getLogger('wsgi')
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler(sys.stderr)
sh.setLevel(logging.DEBUG)

sh.setFormatter(logging.Formatter('[%(levelname)s] %(asctime)s: %(message)s'))

logger.addHandler(sh)


def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    logger.warn(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)
