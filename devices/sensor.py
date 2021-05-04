class Sensor():
    def __init__(self):
        self.__subscribers = []
        self._doc = None

    def attach(self, securitySystem=None):
        print("Attaching")
        # if isinstance(securitySystem, SecuritySystem):
        self.__subscribers.append(securitySystem)

    def trigger(self, state):
        print("Triggering", state)
        for subscriber in self.__subscribers:
            subscriber.publish(self, state)

    def set_doc(self, docRef):
        if docRef:
            self._doc = docRef
