import logging
# import pyserial
import serial
# import json

from channels import Channel
from django.conf import settings


logger = logging.getLogger('wireless adapters')


# Open the serial interface
serial_interface = serial.Serial(
    settings.SERIAL_INTERFACE,
    settings.SERIAL_BAUD,
    timeout=60)

# FIX: this won't work

def serial_response_encode(response):
    return {'response': response}

try:
    while 1:
        response = serial_interface.readline()
        if response:
            Channel('wireless.packet').send(serial_response_encode(response))
except Exception as e:
    logger.error(e)
    serial_interface.close()


# TODO, send a wireless message
