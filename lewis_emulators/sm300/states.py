from lewis.core.statemachine import State


class DefaultState(State):
    def in_state(self, dt):
        device = self._context
        [axis.simulate(dt) for axis in device.axes.values()]
