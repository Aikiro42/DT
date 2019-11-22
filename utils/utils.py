import pyglet


class Clock:
    def __init__(self):
        self.time = 0
        self.interval = 1

    def callback_function(self, *args, **kwargs):
        pass

    def set_interval(self, interval: float):
        self.interval = interval

    def start(self):
        pyglet.clock.schedule(self.callback_function, self.interval)

    def stop(self):
        pyglet.clock.unschedule(self.callback_function)
