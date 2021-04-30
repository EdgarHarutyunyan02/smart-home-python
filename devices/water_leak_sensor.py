from .sensor import Sensor
from gpiozero import DigitalInputDevice
import time


class WaterLeakSensor(Sensor):
    def __init__(self, pin):
        self._input = DigitalInputDevice(
            pin=pin, bounce_time=3, active_state=None, pull_up=True)
        super().__init__()
        self._input.when_activated = lambda: self.trigger(alarm=True)
        self._input.when_deactivated = lambda: self.trigger(alarm=False)
        # while True:
        #     print(self._input.value)
        #     sleep(0.1)
