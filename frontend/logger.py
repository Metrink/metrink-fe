import logging
import sys

logger = logging.getLogger('wsgi')
logger.setLevel(logging.DEBUG)

if len(logger.handlers) == 0:
    sh = logging.StreamHandler(sys.stderr)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s] %(filename)s %(lineno)s:\t%(message)s'))

    logger.addHandler(sh)

