from lewis.core.statemachine import State
import time


class DefaultState(State):
    def in_state(self, dt):
        device = self._context
        device.set_current_time()

        if device.watchdog_refresh_time + 3 < time.time() and device.get_control_mode() != 0:
            print "Watchdog time expired, going back to front panel control mode"
            device.set_control_mode(0)
