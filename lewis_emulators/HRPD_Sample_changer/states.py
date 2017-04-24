from lewis.core import approaches
from lewis.core.statemachine import State


class MovingState(State):
    def on_entry(self, dt):
        self._context.arm_lowered = False

    def in_state(self, dt):
        old_position = self._context.car_pos
        self._context.car_pos = approaches.linear(old_position, self._context.car_target,
                                                   self._context.CAR_SPEED, dt)

    def on_exit(self, dt):
        self._context.arm_lowered = True