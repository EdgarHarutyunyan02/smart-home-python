from .sensor import Sensor


class AmbientSensor(Sensor):
    def __init__(self, event_manager=None, state=None):
        super().__init__()
        self._event_manager = event_manager
        self._event_manager.subscribe("humidity", self._process_humidity_data)

    def _process_humidity_data(self, humidity):
        if type(humidity) == int:
            self.trigger(state=humidity)
            if self._doc:
                self._doc.update(
                    {"states.humidityAmbientPercent": humidity})
