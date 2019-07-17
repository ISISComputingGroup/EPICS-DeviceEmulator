from lewis.core.statemachine import State
from lewis.core import approaches


def get_target_value(device):

    if device.ramp_target == "MID":
        target_value = device.mid_target
    elif device.ramp_target == "MAX":
        target_value = device.max_target
    else:
        target_value = 0

    return target_value


class DefaultInitState(State):

    def in_state(self, dt):
        device = self._context
        device.check_is_at_target()


class HoldingState(State):

    def on_entry(self, dt):
        device = self._context
        print("*********** ENTERED HOLD STATE")
        print(device.output, device.direction)

    def in_state(self, dt):
        device = self._context
        device.check_is_at_target()


class TrippedState(State):

    def in_state(self, dt):
        pass


class RampingState(State):

    def in_state(self, dt):
        device = self._context
        rate = float(device.ramp_rate)
        target = float(get_target_value(device))
        constant = float(device.constant)
        if device.is_output_mode_tesla:
            rate = rate * constant
        device.output = approaches.linear(float(device.output), float(target), float(rate), dt)
        device.check_is_at_target()
