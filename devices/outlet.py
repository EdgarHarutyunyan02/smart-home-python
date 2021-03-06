from threading import Thread, Timer
from time import sleep
from gpiozero import DigitalOutputDevice


class Outlet(DigitalOutputDevice):
    def __init__(self, pin, state=None):
        print("OUTLET_INIT")
        super().__init__(pin, initial_value=False, active_high=False)
        self._doc = None
        if (state):
            self.set_state(state)

    def set_state(self, state, document):
        print("SETTING STATE>>", state)
        if 'on' in state and state['on']:
            self.on()
        else:
            self.off()
        if document:
            self._doc = document
        print("IS_ACTIVE: ", self.is_active)
