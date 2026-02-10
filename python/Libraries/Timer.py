from Libraries.Deltatime import Deltatime


class Timer:

    all_timers = []

    timer = 0

    time_max = 0

    def __init__(self,time,method):

        self.time_max = time

        self.action = method
        
        self.all_timers.append(self)
    
    def time_it(self):
        self.timer += Deltatime.dt

        if (self.timer > self.time_max):
            self.action()
            self.all_timers.remove(self)

    def stop(self):
        self.all_timers.remove(self)

    @classmethod
    def UpdateAllTimers(cls):
        for timer in cls.all_timers[:]:
            timer.time_it()
