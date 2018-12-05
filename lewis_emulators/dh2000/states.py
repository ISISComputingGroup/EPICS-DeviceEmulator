from lewis.core.statemachine import State
from lewis.core.logging import has_log


@has_log
class DefaultState(State):
    def in_state(self, dt):
        device = self._context

        self.log.info('A{:d},I{:d}'.format(device.shutter_is_open, device.interlock_is_triggered))

        if device.interlock_is_triggered and device.shutter_is_open:
            self.log.info("INTERLOCK close shutter")
            device.shutter_is_open = False
