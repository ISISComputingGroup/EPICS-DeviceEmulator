from lewis.core.statemachine import State
import time
from lewis.core import approaches


class DefaultState(State):
    def in_state(self, dt):
        device = self._context
        device.set_current_time()

        if device.watchdog_refresh_time + 3 < time.time() and device.get_control_mode() != 0:
            print "Watchdog time expired, going back to front panel control mode"
            device.set_control_mode(0)

class GoingToSetpointState(DefaultState):
    def in_state(self, dt):
        super(GoingToSetpointState, self).in_state(dt)
        device = self._context
        device.channels[device.control_channel].value = approaches.linear(device.channels[device.control_channel].value,
                                                                          device.channels[device.control_channel].ramp_amplitude_setpoint,
                                                                          0.001, dt)

    def on_exit(self, dt):
        device = self._context
        device._movement_type = 3

