import sender
import logging

from logging.handlers import TimedRotatingFileHandler

class LocalLogger(sender.Sender):
    #_test_diff_file = None
    _local_logger = None
    _local_logger_handler = None

    def __init__(self, queue_size, config=None):
        sender.Sender.__init__(self, queue_size, config)

    def _connect(self, config):
        #self._test_diff_file = open('1.txt','w')
        try:
            logfile = config['log_file']['directory'] + config['log_file']['prefix']
            self._local_logger = logging.getLogger("Local Logger")
            self._local_logger.setLevel(logging.INFO)
            self._local_logger_handler = TimedRotatingFileHandler(logfile,
                                                                  when='m',
                                                                  interval=1,
                                                                  backupCount=7)
            self._local_logger.addHandler(self._local_logger_handler)
        except Exception as e:
            print e
        pass

    def send(self, data):
        print data
        #self._test_diff_file.write(data)
        self._local_logger.info(data)
