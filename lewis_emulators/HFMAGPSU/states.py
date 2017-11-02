from lewis.core.statemachine import State
from lewis.core import approaches


def get_target_value(target, mid_val, max_val):

    if target == "MID":
        target_value = mid_val
    elif target == "MAX":
        target_value = max_val
    else:
        target_value = 0

    return target_value


class DefaultInitState(State):
    pass


class DefaultStoppedState(State):
    def in_state(self, dt):
        pass


class DefaultStartedState(State):
    def in_state(self, dt):
        device = self._context

        rate = float(device._ramp_rate)
        target = float(device._mid_target)
        constant = float(device._constant)

        # conversion logic

        if device._is_output_mode_tesla:
            rate = rate * constant

        device._output = approaches.linear(float(device._output), float(target), float(rate), dt)





