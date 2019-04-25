from lewis.core import approaches
from lewis.core.statemachine import State


class Errors():
    NO_ERR = 0
    ERR_INV_DEST = 5
    ERR_NOT_INITIALISED = 6
    ERR_ARM_DROPPED = 7
    ERR_ARM_UP = 8
    ERR_CANT_ROT_IF_NOT_UP = 10


class MovingState(State):
    def on_entry(self, dt):
        self._context.arm_lowered = False

    def in_state(self, dt):
        old_position = self._context.car_pos
        self._context.car_pos = approaches.linear(old_position, self._context.car_target,
                                                   self._context.CAR_SPEED, dt)

    def on_exit(self, dt):
        self._context.arm_lowered = True
        
