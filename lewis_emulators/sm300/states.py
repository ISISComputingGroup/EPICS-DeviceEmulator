from lewis.core.statemachine import State


class DefaultState(State):
    """
    Default state of the system (it only has one)
    """
    def in_state(self, dt):
        """
        When in this state simulate each axis.
        Args:
            dt: time since last simulate

        """
        device = self._context
        [axis.simulate(dt) for axis in device.axes.values()]
