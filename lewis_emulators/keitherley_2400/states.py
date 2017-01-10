from lewis.core.statemachine import State
from random import random


class DefaultInitState(State):
    pass


class DefaultRunningState(State):
    def in_state(self, dt):
        max_out = 100.0
        self._context.set_current(random*max_out)
        self._context.set_voltage(random*max_out)
        self._context.set_resistance(random*max_out)