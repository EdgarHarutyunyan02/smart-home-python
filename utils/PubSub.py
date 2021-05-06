import threading


class PubSub():
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, channel, callback):
        if not callable(callback):
            raise TypeError("Expected callback function.")
        if channel is None or channel == "":
            raise ValueError("No channel provided.")
        if channel not in self._subscribers.keys():
            self._subscribers[channel] = [callback]
        else:
            self._subscribers[channel].append(callback)

    def unsubscribe(self, channel, callback):
        if channel is not None or channel != "" and channel in self._subscribers.keys():
            self._subscribers[channel] = list(
                filter(
                    lambda fn: fn is not callback,
                    self._subscribers[channel]
                )
            )

    def publish(self, channel, *args, **kwargs):
        threads = []
        if channel in self._subscribers.keys():
            for callback in self._subscribers[channel]:
                threads.append(threading.Thread(
                    target=callback,
                    args=args,
                    kwargs=kwargs
                ))
            for thread in threads:
                thread.start()
