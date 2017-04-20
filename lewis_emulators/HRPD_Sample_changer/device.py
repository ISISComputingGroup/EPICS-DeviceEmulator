from lewis.devices import StateMachineDevice
from lewis.core.statemachine import State
from states import MovingState

from collections import OrderedDict


class SimulatedHRPDSampleChanger(StateMachineDevice):
    NO_ERR = 0
    ERR_INV_DEST = 5
    ERR_NOT_INITIALISED = 6
    ERR_ARM_DROPPED = 7
    ERR_ARM_UP = 8
    ERR_CANT_ROT_IF_NOT_UP = 10

    MIN_CAROUSEL = 1
    MAX_CAROUSEL = 20

    SPEED = 1

    def _initialize_data(self):
        self.car_pos = 0
        self.car_target = 0
        self.arm_lowered = False
        self.current_err = self.NO_ERR

    def _get_state_handlers(self):
        return {
            'init': State(),
            'initialising': MovingState(),
            'idle': State(),
            'moving': MovingState()
        }

    def _get_initial_state(self):
        return 'init'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('init', 'initialising'), lambda: self.car_target != 0),
            (('initialising', 'idle'), lambda: self.car_pos == 1),
            (('idle', 'moving'), lambda: self.car_target != self.car_pos),
            (('moving', 'idle'), lambda: self.car_pos == self.car_target)])

    def get_status(self):
        # Based on the labview VI, appears to be different than doc
        return_string = "01000{0:b}01{1:b}{2:b}{3:b}00000"
        car_at_one = (self.car_pos == self.MIN_CAROUSEL)
        return_string = return_string.format(not self.arm_lowered, car_at_one, not self.arm_lowered, self.arm_lowered)

        return_string += " 0{0:b}1".format(self._csm.state == 'moving')

        return_string += " %02d" % self.current_err
        return_string += " %02d" % self.car_pos

        return return_string

    def go_forward(self):
        if self._csm.state == 'init':
            return self.ERR_NOT_INITIALISED
        if self.arm_lowered:
            return self.ERR_CANT_ROT_IF_NOT_UP
        self.car_target += 1
        if self.car_target > self.MAX_CAROUSEL:
            self.car_target = self.MIN_CAROUSEL
        return self.NO_ERR

    def go_backward(self):
        if self._csm.state == 'init':
            return self.ERR_NOT_INITIALISED
        if self.arm_lowered:
            return self.ERR_CANT_ROT_IF_NOT_UP
        self.car_target -= 1
        if self.car_target < self.MIN_CAROUSEL:
            self.car_target = self.MAX_CAROUSEL
        return self.NO_ERR

    def move_to(self, position, lower_arm):
        if self._csm.state == 'init':
            return self.ERR_NOT_INITIALISED
        if (position < self.MIN_CAROUSEL) or (position > self.MAX_CAROUSEL):
            return self.ERR_INV_DEST
        else:
            self.car_target = position
            self.arm_lowered = lower_arm
            return self.NO_ERR

    def set_arm(self, lowered):
        if self._csm.state == 'init':
            return self.ERR_NOT_INITIALISED
        if lowered == self.arm_lowered:
            if lowered:
                return self.ERR_ARM_DROPPED
            else:
                return self.ERR_ARM_UP
        self.arm_lowered = lowered
        return self.NO_ERR

    def init(self):
        self.arm_lowered = False
        self.car_target = self.MIN_CAROUSEL
        self.current_err = self.NO_ERR
        return self.NO_ERR
