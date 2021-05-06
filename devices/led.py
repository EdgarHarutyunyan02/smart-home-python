from gpiozero import PWMLED
import threading
import queue
from queue import Queue
import numpy as np
from time import sleep


class Led():
    def __init__(self, gpio_pin, state=None):
        print("LED_INIT")
        self._led = PWMLED(pin=gpio_pin, frequency=100)
        self._led.value = 0
        self._brightness_queue = Queue(0)
        self._brightness_thread = None
        self._max_brightness = 0.7
        self._doc = None
        if (state):
            self.set_state(state)

    @property
    def brightness(self):
        return self._pixels.brightness

    @brightness.setter
    def brightness(self, target_brightness=None):
        if target_brightness is None:
            return
        if (self._led.value == target_brightness):
            return
        if target_brightness > self._max_brightness:
            target_brightness = self._max_brightness
        if target_brightness < 0:
            target_brightness = 0

        try:
            self._brightness_queue.put(target_brightness)
        except queue.Full as error:
            print(error)
        if not (self._brightness_thread and self._brightness_thread.is_alive()):
            self._brightness_thread = threading.Thread(
                target=self._change_brightness, daemon=True)
            self._brightness_thread.start()

    def _change_brightness(self):
        while not self._brightness_queue.empty():
            target_brightness = self._brightness_queue.get()
            brightness_from = self._led.value,
            brightness_space = np.linspace(
                brightness_from, target_brightness, 50)
            for brightness in brightness_space:
                self._led.value = brightness[0]
                sleep(0.005)
            self._brightness_queue.task_done()
        return

    def set_state(self, state, document):
        if 'on' in state:
            if state['on'] == False:
                self.brightness = 0
                return
        if state['brightness'] != None:
            self.brightness = state['brightness']/100*self._max_brightness

        if document:
            self._doc = document
