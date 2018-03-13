from lewis.core.statemachine import State


class DefaultState(State):
    """
    Default state of the system (it only has one)
    """
    def in_state(self, dt):
        """
        When in this state simulate ramping to the reading.
        Args:
            dt: time since last simulate

        """
        self._context.simulate(dt)
