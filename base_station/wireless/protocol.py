import time
import logging

logger = logging.getLogger(__name__)


class SerialProtocol(object):
    """
    Protocol that does stuff with serial connections
    """

    def on_connect(self, request):
        self.request_info = {
            "action": request.action,
            # "headers": self.clean_headers,
        }

    def on_open(self):
        self.reply_channel = self.channel_layer.new_channel("!serial.send.?")
        self.request_info["reply_channel"] = self.reply_channel
        self.last_ping = time.time()
        # TODO link factory
        self.factory.reply_protocols[self.reply_channel] = self
        logger.debug("Serial connection open for {}".format(self.reply_channel))
        self.channel_layer.send("serial.connect", self.request_info)

    def on_close(self):
        logger.debug("Serial connection closed for {}".format(self.reply_channel))
        if hasattr(self, "reply_channel"):
            del self.factory.reply_protocols[self.reply_channel]
            self.channel_layer.send("serial.disconnect", {
                "reply_channel": self.reply_channel
            })

    def on_message(self, payload):
        logger.debug("Serial incoming message on {}".format(self.reply_channel))

    def send_message(self, content):
        logger.debug("Sent Serial message to client for {}".format(self.reply_channel))

    def set_ping(self):
        self.channel_layer.send("serial.ping", {
            "reply_channel": self.reply_channel
        })


class SerialFactory(object):

    def __init__(self, channel_layer):
        self.channel_layer = channel_layer
        self.reply_protocols = {}

    def reply_channels(self):
        return self.reply_protocols.keys()

    def dispatch_reply(self, channel, message):
        if isinstance(self.reply_protocols[channel], SerialProtocol):
            self.reply_protocols[channel].send_message(message)
