from threading import Thread, Timer
from time import sleep
from gpiozero import LED


class Lightbulb(LED):
    def __init__(self, pin, state=None):
        super().__init__(pin, initial_value=False)
        self._blinking = False
        self._blink_thread = None
        print("LIGHTBULB_INIT")
        if (state):
            self.set_state(state)
        self._doc = None

    def set_state(self, state, document):
        print("SETTING STATE>>", state)
        if 'on' in state and state['on']:
            self.on()
        else:
            self.off()
        if document:
            self._doc = document
        print("IS_ACTIVE: ", self.is_active)

    def _blink_th(self, turn_on_time, turn_off_time):
        while self._blinking:
            self.on()
            sleep(turn_on_time)
            self.off()
            sleep(turn_off_time)
        return

    def blink(self, turn_on_time=1, turn_off_time=None, timeout=None):
        if turn_off_time is None:
            turn_off_time = turn_on_time
        if not self._blink_thread:
            self._blinking = True
            self._blink_thread = Thread(
                target=_blink_th, args=(turn_on_time, turn_off_time))
        if timeout is not None:
            closing_timer = Timer(timeout, self.stop_blink)

        self._blink_thread.start()

    def stop_blink(self):
        self._blinking = False

