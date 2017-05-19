from lewis.core.statemachine import State


class DefaultState(State):
    def in_state(self, dt):
        device = self._context

        device.set_current_time(dt)

        if device.watchdog_refresh_time + 3 < dt:
            print "Watchdog time expired, going back to front panel control mode"
            device.set_control_mode(0)

