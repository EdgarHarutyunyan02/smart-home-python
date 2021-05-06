from .sensor import Sensor
from gpiozero import Button


class DoorSensor(Sensor):
    def __init__(self, pin):
        super().__init__()
        self._input = Button(pin=pin, hold_time=1,
                             active_state=False, pull_up=None)

        self._input.when_held = lambda: self._process_trigger(state=False)
        self._input.when_released = lambda: self._process_trigger(state=True)

    def _process_trigger(self, **kwargs):
        print("Door sensor state:", kwargs['state'])
        self.trigger(state=kwargs['state'])
        if self._doc:
            self._doc.update(
                {"states.openPercent": 0 if kwargs['state'] == False else 90})
