from .sensor import Sensor
from gpiozero import Button
import time


class WaterLeakSensor(Sensor):
    def __init__(self, pin):
        super().__init__()
        self._input = Button(pin=23, hold_time=1,
                             active_state=False, pull_up=None)

        self._input.when_held = lambda: self._process_trigger(state=True)
        self._input.when_released = lambda: self._process_trigger(state=False)

    def _process_trigger(self, **kwargs):
        self.trigger(state=kwargs['state'])
        # if self._doc:
        self._doc.update(
            {"states.currentSensorStateData.currentSensorState": "leak" if kwargs['state'] == True else "no leak"})
