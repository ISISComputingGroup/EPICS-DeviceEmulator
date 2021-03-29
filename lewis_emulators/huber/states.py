from lewis.core.statemachine import State


class MovingState(State):
    """
    Default state of the system (it only has one)
    """
    def on_entry(self, dt):
        """ Disallow config commands when moving """
        pass


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
