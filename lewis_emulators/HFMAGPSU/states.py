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
        SMALL = 0.00001
        '''
        target = get_target_value(device._ramp_target,
                                  device._zero
                                  device._mid_target,
                                  device._max_target)
        
        # This is now set by SNL file? SNL file finds target and sets MID value
        # to that, so the device is ramping towards an adapted MID target.
        '''
        target = device._mid_target
        rate = device._ramp_rate
        # Starting ramping towards target value
        device._output = approaches.linear(float(device._output), float(target), float(rate), dt)
        # If the output equals the target, trigger not_ramping state with _is_paused variable
        ramp_complete = abs(float(device._output) - float(target)) < SMALL
        if ramp_complete:
            device._is_paused = True



