import zmq
import json
import sender
import snmp_parser
import datetime


class MacTrackerServer(sender.Sender):

    def __init__(self, queue_size, config=None):
        try:
            sender.Sender.__init__(self, queue_size, config)
            self._config = config
        except Exception as e:
            print e

    def _connect(self, config):
        self._port = int(self._config['port'])
        self._parser = snmp_parser.Parser()

        self._context = zmq.Context()
        self._tracker_server = self._context.socket(zmq.PUB)
        self._tracker_server.bind("tcp://*:%s" % self._port)

    def _process_data(self, data):
        event_json = self._parser.parse(data)
        event_json['time'] = str(datetime.datetime.now())
        return event_json

    def send(self, data_processed):
        topic = data_processed["client_mac"]
        message_data = str(data_processed["time"]) + "   " + str(data_processed["ap_id"])
        self._tracker_server.send("%s %s" % (topic, message_data))
