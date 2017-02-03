import mock
import os
import logging

logger = logging.getLogger()

DEBUG = os.getenv('DEBUG', False)

if DEBUG:
    GPIO = mock.MagicMock()
else:
    import RPi.GPIO as GPIO


class RPiGPIO:

    relays = (
        26, 19, 13, 6
    )

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for pin in self.relays:
            GPIO.setup(pin, GPIO.OUT)

    def _set_pin(self, pin, state):
        logger.info('set pin %s to %s', pin, state)
        GPIO.output(pin, state)

    def on(self, pin):
        self._set_pin(pin, 1)

    def off(self, pin):
        self._set_pin(pin, 0)


if __name__ == '__main__':
    def read_input():
        gpio = RPiGPIO()
        while True:
            relay = int(input("Relay: "))
            state = int(input("State: "))
            try:
                gpio._set_pin(RPiGPIO.relays[RPiGPIO.relays.index(relay)], int(state))
            except ValueError:
                logger.error("Relay doesn't exist")

    read_input()
