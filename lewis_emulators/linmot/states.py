import math

from lewis.core.statemachine import State
from lewis.core import approaches


class StoppedState(State):
    pass


class MovingState(State):

    def in_state(self, dt):
        device = self._context
        device.position = approaches.linear(device.position, device.target_position, (device.maximal_speed / 1e6 * device.speed_resolution), dt)
        if abs(device.target_position - device.position) <= device.tolerance:
            device.position_reached = True

