import math

from lewis.core.statemachine import State
from lewis.core import approaches


class StoppedState(State):

    def in_state(self, dt):
        device = self._context
        device.is_within_hard_limits()


class MovingState(State):

    def in_state(self, dt):
        device = self._context
        device.position = approaches.linear(device.position, device.target_position, device.velocity, dt)
        device.is_within_hard_limits()
        if abs(device.target_position - device.position) <= device.tolerance:
            device.position_reached = True


class ErrorState(State):
    pass
