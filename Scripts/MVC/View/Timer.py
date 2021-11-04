import time

class Timer():
    def __init__(self):
        self.elapsed = 0.0
        self._startTime = 0.0
        self._stopTime = 0.0

    def start(self):
        self._startTime = time.perf_counter()

    def stop(self):
        self._stopTime = time.perf_counter()
        self.elapsed = self._stopTime - self._startTime
        return self.elapsed