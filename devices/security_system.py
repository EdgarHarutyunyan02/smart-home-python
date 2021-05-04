from gpiozero import LED
from .water_leak_sensor import WaterLeakSensor


class SecuritySystem(LED):
    def __init__(self, state_pin, buzzer_pin, state=None):
        super().__init__(state_pin, initial_value=False)
        self.__state = state
        self.__alarm = False
        self.__alarm_indicator = LED(buzzer_pin, initial_value=False)
        self.__doc = None

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
            self.__doc = document

    def set_alarm(self, value):
        self.__alarm = value
        if value == True:
            self.__alarm_indicator.blink(
                on_time=0.3, off_time=0.2, background=True)
            self.__doc.update({"states.isArmed": True})
        else:
            self.__alarm_indicator.off()

    def publish(self, sensor, alarm):
        if isinstance(sensor, WaterLeakSensor):
            if alarm == True:
                # Water leak detected, turn on the alarm.
                self.set_alarm(True)
                return

        if isinstance(sensor, WaterLeakSensor):
            if (self.state['isArmed']):
                pass
            pass
