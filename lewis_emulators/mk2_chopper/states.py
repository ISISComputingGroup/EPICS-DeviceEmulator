from lewis.core.statemachine import State
from lewis.core import approaches

def output_current_state(device, state_name):
    print "{0}: Freq {1}, Phase {2}, Error {3}".format(state_name.upper(),
                                      device.get_true_frequency(),
                                      device.get_true_phase_delay(),
                                      device.get_true_phase_error())

class DefaultInitState(State):
    pass


class DefaultStoppedState(State):
    def in_state(self, dt):
        device = self._context
        output_current_state(self._context, "stopped")
        device.set_true_frequency(approaches.linear(device.get_true_frequency(), 0, 1, dt))


class DefaultStartedState(State):
    def in_state(self, dt):
        device = self._context
        output_current_state(self._context, "started")
        device.set_true_frequency(approaches.linear(device.get_true_frequency(),
                                                    device.get_demanded_frequency(), 1, dt))
