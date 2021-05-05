from .sensor import Sensor
import time


class TemperatureSensor(Sensor):
    def __init__(self, event_manager=None):
        super().__init__()
        self._event_manager = event_manager
        self._event_manager.subscribe("temperature", self._process_temp_data)
        self._last_time_updated_doc = None
        self._report_interval = 30

    def _process_temp_data(self, temperature):
        print("Processing temperature Data:", temperature)
        if type(temperature) == int:
            self.trigger(state=temperature)
            if self._doc:
                if self._last_time_updated_doc == None or (time.time() - self._last_time_updated_doc) > self._report_interval:
                    self._last_time_updated_doc = time.time()
                    self._doc.update(
                        {"states.temperatureAmbientCelsius": temperature})
