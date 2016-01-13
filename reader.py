import threading
import sys
import time

class Reader (threading.Thread):
    _pipe_file_location = None
    _pipe_file = None
    _broker = None

    def __init__(self, broker, config):
        threading.Thread.__init__(self)
        self._pipe_file_location = config["location"]
        self._broker = broker

        try:
            self._pipe_file = open(self._pipe_file_location, 'r')
        except IOError:
            #sys.stdout.write("ERROR: Can\'t open pipe file.\n")
            print "ERROR: Can\'t open pipe file."

        return

    def run(self):
        while(True):
            try:
                data_line = self._pipe_file.readline()#[:-1]
            except Exception as e:
                print e
                print "ERROR: Can\'t read line from pipe file"
                time.sleep(1)
            if data_line != '':
                #print data_line
                try:
                    self._broker.get(data_line)
                except Exception as e:
                    print e
                    #sys.stdout.write("Error: PipeReader is unable to push data to Broker\n")
                    print "Error: PipeReader is unable to push data to Broker\n"




