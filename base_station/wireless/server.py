"""
Ideas, serial server is it's own module like daphean, allows you to place different
serial protocols in place of a byte streaming one.

The module has a CLI Server that accepts the serial port/buad rate + any other config.
"""

from .protocol import SerialFactory

class Server(object):

    def __init__(self, channel_layer, interface='/dev/null', baud=False):
        self.channel_layer = channel_layer
        self.interface = interface
        self.baud = baud

    def run(self):
        self.factory = SerialFactory(self.channel_layer)

    def backend_render(self):
        while True:
            channels = self.factory.reply_channels()
            # Quit if reactor is stopping
            if not reactor.running:
                return
            # Don't do anything if there's no channels to listen on
            if channels:
                channel, message = self.channel_layer.receive_many(channels, block=True)
            else:
                time.sleep(0.1)
                continue
            # Wait around if there's nothing received
            if channel is None:
                time.sleep(0.05)
                continue
            # Deal with the message
            self.factory.dispatch_reply(channel, message)

    def keepalive_sender(self):
