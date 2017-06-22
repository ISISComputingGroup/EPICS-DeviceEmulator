from lewis.core.statemachine import State
import time
from lewis.core import approaches


class DefaultState(State):
    TIME_SINCE_LAST_QUART_COUNT = 0

    def in_state(self, dt):
        device = self._context
        device.set_current_time()

        if device.watchdog_refresh_time + 3 < time.time() and device.get_control_mode() != 0:
            print "Watchdog time expired, going back to front panel control mode"
            device.set_control_mode(0)

        device.stop_waveform_generation_if_requested()

        GoingToSetpointState.TIME_SINCE_LAST_QUART_COUNT += dt
        if GoingToSetpointState.TIME_SINCE_LAST_QUART_COUNT > 1.0:
            GoingToSetpointState.TIME_SINCE_LAST_QUART_COUNT = 0.0
            device.quarter_cycle_event()


class GoingToSetpointState(DefaultState):

    def in_state(self, dt):
        super(GoingToSetpointState, self).in_state(dt)
        device = self._context
        device.channels[device.control_channel].value = approaches.linear(device.channels[device.control_channel].value,
                                                                          device.channels[device.control_channel].ramp_amplitude_setpoint,
                                                                          0.001, dt)