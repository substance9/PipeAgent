import time
import os


class Buffer(object):
    _first_pipe_location = "/home/clyde/snmptrapd.log"
    _second_pipe_location = "../buffer"
    _first_pipe = None
    #_second_pipe = None
    _second_pipe_fd = None

    _second_pipe_writable = False

    def __init__(self):
        try:
            self._first_pipe = open(self._first_pipe_location, 'r')
        except Exception as e:
            print e
            print "ERROR: Can\'t open first pipe file"

        self._open_second_pipe()

        pass

    def _open_second_pipe(self):
        try:
            self._second_pipe_fd = os.open(self._second_pipe_location, os.O_WRONLY|os.O_NONBLOCK)
        except Exception as e:
            print e
            print "ERROR: Can\'t open second pipe file"
        else:
            self._second_pipe_writable = True



    def run(self):
        while(True):
            try:
                data_line = self._first_pipe.readline()
                #with open(self._first_pipe_location, 'r') as first_pipe:
                #    data_line = first_pipe.readline()
            except Exception as e:
                print e
                print "ERROR: Can\'t read line from first pipe file"
                time.sleep(1)
                continue
            else:
                if data_line != '':
                    if self._second_pipe_writable is True:
                        try:
                            #with os.fdopen(os.open(self._second_pipe_location, os.O_WRONLY|os.O_NONBLOCK)) as second_pipe:
                            #self._second_pipe.write(data_line)
                            os.write(self._second_pipe_fd, data_line)
                        except Exception as e:
                            print e
                            print "ERROR: Can\'t Write line to second pipe file"
                            self._second_pipe_writable = False
                        else:
                            print data_line
                    # if second pipe file is not writable
                    else:
                        self._open_second_pipe()


if __name__ == '__main__':
    pbuffer = Buffer()
    pbuffer.run()
