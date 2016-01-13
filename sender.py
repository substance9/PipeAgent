import threading
import Queue


class Sender(threading.Thread):
    _queue = None
    _config = None

    def __init__(self, queue_size=4096, config=None):
        threading.Thread.__init__(self)
        self._queue = Queue.Queue(queue_size)
        self._config = config
        self._connect(self._config)

    def _connect(self, config):
        raise NotImplementedError()

    def get(self, data):
        self._on_get_data(data)

    def _on_get_data(self, data):
        self._queue.put(data)

    def _process_data(self, data):
        return data

    def send(self, data):
        raise NotImplementedError()

    def run(self):
        while(True):
            data = self._queue.get(block=True)
            #TODO: I am not sure if the blocking queue will cause any issue. Need to be studied carefully. If use non-blocking queue, need to handle the empty exception
            processed_data = self._process_data(data)
            self.send(processed_data)

