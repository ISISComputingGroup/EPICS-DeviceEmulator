from lewis.core.statemachine import State


class DefaultState(State):
    def in_state(self, dt):
        device = self._context
        device.x_axis.simulate(dt)
        device.y_axis.simulate(dt)
