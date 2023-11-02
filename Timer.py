class Timer:
    _seconds: int

    def __init__(self, initSeconds = 0):
        self._seconds = max(initSeconds, 0)

    @property
    def seconds(self): return self._seconds

    @property
    def isStopped(self): return self.seconds == 0

    def reset(self, toSeconds): self._seconds = max(toSeconds, 0)

    def update(self, secondsElapsed: int = 1):
        if not self.isStopped:
            self._seconds -= max(secondsElapsed, 0)


