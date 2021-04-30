# from threading import Thread, Timer
#from devices import SecuritySystem
# from devices.security_system import SecuritySystem


class Sensor():
    def __init__(self):
        self.__subscribers = []

    def attach(self, securitySystem=None):
        print("Attaching")
        # if isinstance(securitySystem, SecuritySystem):
        self.__subscribers.append(securitySystem)

    def trigger(self, alarm):
        print("Triggering", alarm)
        for subscriber in self.__subscribers:
            subscriber.publish(self, alarm=alarm)

    # @property
    # # Getter method
    # def state(self):
    #     return self.__state

    # @state.setter
    # def state(self, value):
    #     self.__state = value

    # def set_state(self, state):
    #     self.__state = state
    #     return
    #     print("SETTING STATE>>", state)
    #     if 'on' in state and state['on']:
    #         self.on()
    #     else:
    #         self.off()
    #     print("IS_ACTIVE: ", self.is_active)

    # def _blink_th(self, turn_on_time, turn_off_time):
    #     while self._blinking:
    #         self.on()
    #         sleep(turn_on_time)
    #         self.off()
    #         sleep(turn_off_time)
    #     return

    # def blink(self, turn_on_time=1, turn_off_time=None, timeout=None):
    #     if turn_off_time == None:
    #         turn_off_time = turn_on_time
    #     if not self._blink_thread:
    #         self._blinking = True
    #         self._blink_thread = Thread(
    #             target=_blink_th, args=(turn_on_time, turn_off_time))
    #     if timeout != None:
    #         closing_timer = Timer(timeout, self.stop_blink)

    #     self._blink_thread.start()

    # def stop_blink(self):
    #     self._blinking = False

    # pass
