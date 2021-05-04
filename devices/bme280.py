import busio
import adafruit_bme280
import time
import threading
import board
import queue
from queue import Queue


class BME280():
    def __init__(self, event_manager):
        self.interval = 30
        self._monitoring_thread = None
        self._subscribers = Queue()
        self._temperature = None
        self._pressure = None
        self._humidity = None
        self._altitude = None
        self._monitor_th = False
        self._event_manager = event_manager

        i2c = busio.I2C(board.SCL, board.SDA)
        self._sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        self._sensor.sea_level_pressure = 1013.25

    def _monitor_thread(self):
        while True:
            self._temperature = int(self._sensor.temperature)
            self._pressure = int(self._sensor.pressure)
            self._humidity = int(self._sensor.humidity)
            self._altitude = int(self._sensor.altitude)
            self._event_manager.publish("temperature", self._temperature)
            self._event_manager.publish("humidity", self._humidity)
            self._event_manager.publish("pressure", self._pressure)
            self._event_manager.publish("altitude", self._altitude)
            time.sleep(self.interval)

    def start_monitoring(self):
        self._monitoring_thread = threading.Thread(
            target=self._monitor_thread, daemon=True)
        self._monitoring_thread.start()

    def stop_monitoring(self):
        self._monitoring_thread.stop()
