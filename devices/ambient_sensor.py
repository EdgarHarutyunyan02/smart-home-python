from .sensor import Sensor
import time


class AmbientSensor(Sensor):
    def __init__(self, event_manager=None, state=None):
        super().__init__()
        self._event_manager = event_manager
        self._event_manager.subscribe("humidity", self._process_humidity_data)
        self._last_time_updated_doc = None
        self._report_interval = 30

    def _process_humidity_data(self, humidity):
        if type(humidity) == int:
            self.trigger(state=humidity)
            if self._doc:
                if self._last_time_updated_doc == None or (time.time() - self._last_time_updated_doc) > self._report_interval:
                    self._last_time_updated_doc = time.time()
                    self._doc.update(
                        {"states.humidityAmbientPercent": humidity})
