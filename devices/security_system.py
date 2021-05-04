from gpiozero import LED
from .water_leak_sensor import WaterLeakSensor
from .temperature_sensor import TemperatureSensor
from .ambient_sensor import AmbientSensor


class SecuritySystem(LED):
    def __init__(self, state_pin, buzzer_pin, state=None):
        super().__init__(state_pin, initial_value=False)
        self.__state = state
        self.__alarm = False
        self.__alarm_indicator = LED(buzzer_pin, initial_value=False)
        self._doc = None

    @property
    def state(self):
        return self.__state

    def set_state(self, state, document):
        print("Setting Security System State", state)
        self.__state = state
        if "isArmed" in state and state['isArmed']:
            self.on()
        else:
            self.set_alarm(False)
            self.off()

        if document:
            self._doc = document

    def set_alarm(self, value):
        self.__alarm = value
        if value == True:
            self.__alarm_indicator.blink(
                on_time=0.3, off_time=0.2, background=True)
            self._doc.update({"states.isArmed": True})
        else:
            self.__alarm_indicator.off()

    def publish(self, sensor, state):
        if isinstance(sensor, WaterLeakSensor):
            if state == True:
                # Water leak detected, turn on the alarm.
                self.set_alarm(True)
                return

        if isinstance(sensor, TemperatureSensor):
            if type(state) is int:
                if state > 35:
                    # Temperature got high
                    self.set_alarm(True)
                    return

        if isinstance(sensor, AmbientSensor):
            if type(state) is int:
                if not (40 <= state <= 60):
                    # Humidity is not normal
                    self.set_alarm(True)
                    return
