from .sensor import Sensor


class TemperatureSensor(Sensor):
    def __init__(self, event_manager=None):
        super().__init__()
        self._event_manager = event_manager
        self._event_manager.subscribe("temperature", self._process_temp_data)

    def _process_temp_data(self, temperature):
        print("Processing temperature Data:", temperature)
        if type(temperature) == int:
            self.trigger(state=temperature)
            if self._doc:
                self._doc.update(
                    {"states.temperatureAmbientCelsius": temperature})
