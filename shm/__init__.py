import logging
import sys
import socket

FORMAT = '%(asctime)-15s ' + socket.gethostname() + ' PID=%(process)d: %(message)s'
logging.basicConfig(format=FORMAT, stream=sys.stderr, level=logging.INFO)

logging.info("Logging is initialized")