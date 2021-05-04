import neopixel
import threading
import queue
from queue import Queue
import numpy as np
from time import sleep


class RGBLed():
    def __init__(self, data_pin, pixel_count, state=None):
        print("RGB_INIT")
        self._pixels = neopixel.NeoPixel(data_pin, pixel_count)
        self._pixels.brightness = 0
        self._color = (0, 0, 0)
        self._brightness_queue = Queue(0)
        self._color_queue = Queue(0)
        self._transition_thread = None
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
        if (self._pixels.brightness == target_brightness):
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

        # print("Brightness target: ", target_brightness)
        # self._brightness_thread = threading.Thread(
        #     target=self._change_brightness, args=(self._pixels.brightness, target_brightness))
        # self._brightness_thread.start()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, target_color=None):
        if target_color is None:
            return
        if not isinstance(target_color, tuple):
            target_color = self._hex_to_rgb(target_color)
        if (self._color == target_color):
            return

        try:
            self._color_queue.put(target_color)
        except queue.Full as error:
            print(error)

        if not (self._transition_thread and self._transition_thread.is_alive()):
            self._transition_thread = threading.Thread(
                target=self._change_color, daemon=True)
            self._transition_thread.start()

    def _hex_to_rgb(self, hex):
        h = hex.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _change_color(self):
        while not self._color_queue.empty():
            color_from = self._color
            target_color = self._color_queue.get()
            colors = np.int_(np.linspace(color_from, target_color, 100))
            for color in colors:
                self._pixels.fill(tuple(color))
                self._color = tuple(color)
                sleep(0.005)
            self._color_queue.task_done()
        return

    def _change_brightness(self):
        while not self._brightness_queue.empty():
            target_brightness = self._brightness_queue.get()
            brightness_from = self._pixels.brightness,
            brightness_space = np.linspace(
                brightness_from, target_brightness, 50)
            for brightness in brightness_space:
                self._pixels.brightness = brightness[0]
                sleep(0.005)
            self._brightness_queue.task_done()
        return

    def set_state(self, state, document):
        print("SETTING STATE>>", state['color']['spectrumRgb'])
        if state['color']['spectrumRgb'] != None:
            self.color = self._hex_to_rgb(state['color']['spectrumRgb'])
        if 'on' in state:
            if state['on'] == False:
                self.brightness = 0
                return

        if state['brightness'] != None:
            self.brightness = state['brightness']/100*self._max_brightness

        if document:
            self._doc = document
