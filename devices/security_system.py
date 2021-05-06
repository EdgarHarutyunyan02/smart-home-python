from gpiozero import LED
from .water_leak_sensor import WaterLeakSensor
from .temperature_sensor import TemperatureSensor
from .ambient_sensor import AmbientSensor
from .door_sensor import DoorSensor

from datetime import datetime


class SecuritySystem(LED):
    def __init__(self, state_pin, buzzer_pin, event_manager, state=None):
        super().__init__(state_pin, initial_value=False)
        self._state = state
        self._alarm = False
        self._alarm_indicator = LED(buzzer_pin, initial_value=False)
        self._event_manager = event_manager
        self._doc = None

    @property
    def state(self):
        return self._state

    def set_state(self, state, document):
        print("Setting Security System State", state)
        self._state = state
        if "isArmed" in state and state['isArmed']:
            self.on()
        else:
            self.set_alarm(False)
            self.off()
        print("ARNED_STATUS:", self._state["isArmed"])
        if document:
            self._doc = document

    def set_alarm(self, value, description=""):
        if self._alarm == False and value == True:
            # Changed from False to True, Notify user.
            try:
                time_string = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                message = f'''
                        Your security alarm was triggered at: {time_string}.
                        {description}
                        '''
                self._event_manager.publish(
                    "SEND_MESSAGE", message, "Security System")
            except Exception as error:
                print(error)

        self._alarm = value
        if value == True:
            self._alarm_indicator.blink(
                on_time=0.3, off_time=0.2, background=True)
            if self._doc:
                self._doc.update({"states.isArmed": True})
        else:
            self._alarm_indicator.off()

    def publish(self, sensor, state):
        if isinstance(sensor, WaterLeakSensor):
            if state == True:
                # Water leak detected, turn on the alarm.
                self.set_alarm(True, description="Water leak detected.")
                return

        if isinstance(sensor, TemperatureSensor):
            if type(state) is int:
                if state > 35:
                    # Temperature got high
                    self.set_alarm(
                        True, description="Temperature is above 35 Celsius.")
                    return

        if isinstance(sensor, AmbientSensor):
            if type(state) is int:
                # Humidity is not normal
                if state < 40:
                    self.set_alarm(
                        True, description="Humidity is below 40%")
                if state > 70:
                    self.set_alarm(
                        True, description="Humidity is above 70%")
                    return

        if isinstance(sensor, DoorSensor):
            if type(state) is bool:
                if self._state and self._state["isArmed"] == True:
                    if state == True:
                        # Door is open
                        self.set_alarm(
                            True, description="Door is open.")
