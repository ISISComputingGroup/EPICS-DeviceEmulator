from lewis.core.statemachine import State
from math import floor


class StoppedState(State):

    def on_entry(self, dt):
        self._context.state = StoppedState.__name__


class IdleState(State):

    def on_entry(self, dt):
        self._context.state = IdleState.__name__


class InitialisedState(State):

    def on_entry(self, dt):
        self._context.state = InitialisedState.__name__


class OscillatingState(State):

    def on_entry(self, dt):
        dev = self._context
        dev.state = OscillatingState.__name__
        self.time = 0.0
        self.new_cycle = False

    @staticmethod
    def total_cycle_time(width, speed, acceleration):
        transition_time = speed/acceleration
        window_time = width/speed
        return 2*transition_time + window_time

    def in_state(self, dt):
        self.time += dt
        dev = self._context
        dev.complete_cycles = floor(self.time/self.total_cycle_time(dev.window_width, dev.speed, dev.acceleration))


class IdleState(State):

    def on_entry(self, dt):
        self._context.state = IdleState.__name__


class InitialisedState(State):

    def on_entry(self, dt):
        self._context.state = InitialisedState.__name__


class InitialisingState(State):

    def on_entry(self, dt):
        self._context.state = InitialisingState.__name__
        self._context.initialisation_requested = False

    def in_state(self, dt):
        self._context.time_spent_initialising += dt

    def on_exit(self, dt):
        self._context.stop_initialisation = False
        self._context.time_spent_initialising = 0.0


class ResetState(State):

    def on_entry(self, dt):
        dev = self._context
        dev.window_width = 100
        dev.acceleration = 500
        dev.speed = 20
        dev.offset = 0
        dev.initialisation_requested = False
        dev.start_requested = False
        dev.stop_initialisation = False
        dev.complete_cycles = 0
        dev.reset = False
