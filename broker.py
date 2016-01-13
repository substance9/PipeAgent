import threading
import time


class Broker (threading.Thread):
    _sender_list = []

    def __init__(self):
        threading.Thread.__init__(self)

        pass

    def get(self, data):
        self._on_get_data(data)

    def _on_get_data(self, data):
        # test use
        #print data

        #TODO: Push data to sender list
        for sender in self._sender_list:
            sender.get(data)
        return

    def register_sender(self, sender):
        self._sender_list.append(sender)
        return

    def run(self):
        while True:
            time.sleep(1)
            pass


