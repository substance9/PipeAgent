import sys
import time
import yaml
import logging
import threading

from broker import Broker
from reader import Reader
from locallogger import LocalLogger
from mac_tracker_server import MacTrackerServer


class PipeAgent(threading.Thread):
    _config = None

    def __init__(self, config=None):
        threading.Thread.__init__(self)
        if config is None:
            #sys.stdout.write("Error: Config file empty or not initialized\n")
            print "Error: Config file empty or not initialized\n"
            return

        self._config = config

    def run(self):
        # 1. Start Broker
        broker = Broker()
        broker.setDaemon(True)
        broker.start()

        # 2. Start Senders
        try:
            local_logger = LocalLogger(
                queue_size=4096,
                config=self._config['sender']['local_logger'])
            local_logger.setDaemon(True)
        except Exception as e:
            print e
            print "ERROR: Can\'t create local looger"
        else:
            broker.register_sender(local_logger)
            local_logger.start()

        try:
            mac_tracker_server = MacTrackerServer(
                queue_size=4096,
                config=self._config['sender']['mac_tracker_server']
            )
            mac_tracker_server.setDaemon(True)
        except Exception as e:
            print e
            print "ERROR: Can\'t create MAC tracker server"
        else:
            broker.register_sender(mac_tracker_server)
            mac_tracker_server.start()

        # 3. Start Reader
        try:
            reader = Reader(broker, config=self._config['pipe_file'])
            reader.setDaemon(True)
        except Exception as e:
            #sys.stdout.write("Error: Can\'t create PipeReader\n")
            print e
            print "Error: Can\'t create PipeReader\n"
        else:
            reader.start()

        broker.join()
        reader.join()


        #Agent Thread Start Idle Here
        while (True):
            time.sleep(1)
            pass

def main(args=None):
    #global log
    #log = logging.getLogger()
    try:
        config_file = open('config.yml')
    except IOError:
        #sys.stdout.write("Error: can\'t find config file or read data from: config.yml\n")
        print "Error: can\'t find config file or read data from: config.yml\n"
        return
    else:
        config_map = yaml.load(config_file)
        config_file.close()

    agent = PipeAgent(config=config_map)
    agent.setDaemon(True)
    agent.start()

    # Main Thread Idle Here
    while (True):
        time.sleep(1)

if __name__ == "__main__":
    main()

