from lewis.devices import Device


class SimulatedHRPDSampleChanger(Device):
    NO_ERR = 0
    ERR_INV_DEST = 5
    ERR_ARM_DROPPED = 7
    ERR_ARM_UP = 8
    ERR_CANT_ROT_IF_NOT_UP = 10

    MIN_CAROUSEL = 1
    MAX_CAROUSEL = 20

    carousel_position = MIN_CAROUSEL
    arm_lowered = False
    current_err = NO_ERR

    def get_status(self):
        # Based on the labview VI, appears to be different than doc
        return_string = "00000{0:b}01{1:b}{2:b}{3:b}00000 000"
        car_at_one = (self.carousel_position == self.MIN_CAROUSEL)
        return_string = return_string.format(not self.arm_lowered, car_at_one, not self.arm_lowered, self.arm_lowered)
        return_string += " %02d" % self.current_err
        return_string += " %02d" % self.carousel_position
        return return_string

    def go_forward(self):
        if self.arm_lowered:
            return self.ERR_CANT_ROT_IF_NOT_UP
        self._device.carousel_position += 1
        if self._device.carousel_position > self.MAX_CAROUSEL:
            self._device.carousel_position = self.MIN_CAROUSEL
        return self.NO_ERR

    def go_backward(self):
        if self.arm_lowered:
            return self.ERR_CANT_ROT_IF_NOT_UP
        self._device.carousel_position -= 1
        if self._device.carousel_position < self.MIN_CAROUSEL:
            self._device.carousel_position = self.MAX_CAROUSEL
        return self.NO_ERR

    def move_to(self, position, lower_arm):
        if (position < self.MIN_CAROUSEL) or (position > self.MAX_CAROUSEL):
            return self.ERR_INV_DEST
        else:
            self.carousel_position = position
            self.arm_lowered = lower_arm
            return self.NO_ERR

    def set_arm(self, lowered):
        if lowered != self.arm_lowered:
            if lowered:
                return self.ERR_ARM_DROPPED
            else:
                return self.ERR_ARM_UP
        self.arm_lowered = lowered
        return self.NO_ERR

    def init(self):
        self.arm_lowered = False
        self.carousel_position = self.MIN_CAROUSEL
        self.current_err = self.NO_ERR
        return self.NO_ERR
