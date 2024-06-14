from lewis.core import approaches
from lewis.core.statemachine import State


RATE = 10


class TemperatureControlState(State):
    def in_state(self, dt):
        device = self._context

        device.he3pot_temp = approaches.linear(
            device.he3pot_temp, device.temperature_sp, RATE, dt
        )


class He3PotEmptyState(State):

    def in_state(self, dt):
        device = self._context

        device.sorb_temp = approaches.linear(
            device.sorb_temp, device.temperature_sp, RATE, dt
        )
        device.he3pot_temp = approaches.linear(
            device.he3pot_temp, device.he3pot_empty_drift_towards, device.drift_rate, dt
        )


class RegeneratingState(State):

    def in_state(self, dt):
        device = self._context

        device.sorb_temp = approaches.linear(
            device.sorb_temp, device.temperature_sp, RATE, dt
        )
        device.he3pot_temp = approaches.linear(
            device.he3pot_temp, device.he3pot_regenerating_drift_towards, device.drift_rate, dt
        )
