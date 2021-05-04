from .sensor import Sensor
from gpiozero import Button
import time


class WaterLeakSensor(Sensor):
    def __init__(self, pin):
        self._input = Button(pin=23, hold_time=1,
                             active_state=False, pull_up=None)

        super().__init__()
        self._input.when_held = lambda: self.trigger(alarm=True)
        self._input.when_released = lambda: self.trigger(alarm=False)
        # while True:
        #     print(self._input.value)
        #     sleep(0.1)
