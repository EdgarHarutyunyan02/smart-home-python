from gpiozero import LED
from .water_leak_sensor import WaterLeakSensor
from .temperature_sensor import TemperatureSensor
from .ambient_sensor import AmbientSensor

from utils.MailService import MailService
from datetime import datetime


class SecuritySystem(LED):
    def __init__(self, state_pin, buzzer_pin, state=None):
        super().__init__(state_pin, initial_value=False)
        self.__state = state
        self.__alarm = False
        self.__alarm_indicator = LED(buzzer_pin, initial_value=False)
        self._doc = None
        self._mail_service = MailService()

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

    def set_alarm(self, value, description=""):
        if self.__alarm == False and value == True:
            # Changed from False to True, Notify user.
            try:
                time_string = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                message = f'''
                        Your security alarm was triggered at: {time_string}.
                        {description}
                        '''
                self._mail_service.send_message(message, "Security System")
            except Exception as error:
                print(error)

        self.__alarm = value
        if value == True:
            self.__alarm_indicator.blink(
                on_time=0.3, off_time=0.2, background=True)
            if self._doc:
                self._doc.update({"states.isArmed": True})
        else:
            self.__alarm_indicator.off()

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
