import threading


class LocalLogger(threading.Thread):


    def __init__(self):
        threading.Thread.__init__(self)
