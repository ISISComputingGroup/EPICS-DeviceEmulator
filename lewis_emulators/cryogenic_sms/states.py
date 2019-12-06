from lewis.core.statemachine import State
from lewis.core import approaches
from lewis.core.logging import has_log


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


@has_log
class HoldingState(State):

    def on_entry(self, dt):
        self.log.info("*********** ENTERED HOLD STATE")

    def in_state(self, dt):
        device = self._context
        device.check_is_at_target()


class TrippedState(State):

    def in_state(self, dt):
        pass


class RampingState(State):

    def in_state(self, dt):
        device = self._context
        rate = device.ramp_rate
        target = device.ramp_target_value()
        constant = device.constant
        if device.is_output_mode_tesla:
            rate = rate * constant
        device.output = approaches.linear(device.output, target, rate, dt)
        device.check_is_at_target()
