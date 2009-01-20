import logging
import xmpphandler
import time
import sys

logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s %(levelname)s - %(message)s")
handler = xmpphandler.XMPPHandler(logging.DEBUG, sys.argv[1], sys.argv[2])
handler.setFormatter(formatter)
logger.addHandler(handler)

for i in range(3):
    logger.debug('i = %d' % 1)
    time.sleep(3)

