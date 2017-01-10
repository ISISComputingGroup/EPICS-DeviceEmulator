from lewis.core.statemachine import State
from random import uniform


class DefaultInitState(State):
    pass


class DefaultRunningState(State):
    def in_state(self, dt):
        def get_next_value(get_method):
            return abs(get_method() + uniform(-1,1)*dt)
        getters_and_setters = [
            (self._context.set_current,self._context.get_current),
            (self._context.set_voltage,self._context.get_voltage),
            (self._context.set_resistance,self._context.get_resistance),
        ]
        for gs in getters_and_setters:
            gs[0](get_next_value(gs[1]))
