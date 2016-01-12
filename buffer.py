import time
import os


class Buffer(object):
    _first_pipe_location = "pipe"
    _second_pipe_location = "buffer"
    _first_pipe = None
    _second_pipe = None

    def __init__(self):
        try:
            self._first_pipe = open(self._first_pipe_location, 'r')
        except Exception as e:
            print e
            print "ERROR: Can\'t open first pipe file"

        try:
            self._second_pipe = open(self._second_pipe_location, 'w')
        except Exception as e:
            print e
            print "ERROR: Can\'t open second pipe file"

        pass


    def run(self):
        while(True):
            try:
                data_line = self._first_pipe.readline()[:-1]
                #with open(self._first_pipe_location, 'r') as first_pipe:
                #    data_line = first_pipe.readline()
            except Exception as e:
                print e
                print "ERROR: Can\'t read line from first pipe file"
                time.sleep(1)
                continue
            else:
                if data_line != '':
                    try:
                        #with os.fdopen(os.open(self._second_pipe_location, os.O_WRONLY|os.O_NONBLOCK)) as second_pipe:
                        self._second_pipe.write(data_line)
                    except Exception as e:
                        print e
                        print "ERROR: Can\'t Write line to second pipe file"



if __name__ == '__main__':
    buffer = Buffer()
    buffer.run()