from lewis.core import approaches
from lewis.core.statemachine import State


class TemperatureControlState(State):
    def in_state(self, dt):
        device = self._context

        rate = 10

        device.temperature = approaches.linear(device.temperature, device.temperature_sp, rate, dt)


class He3PotEmptyState(State):

    DRIFT_TOWARDS = 1.5  # When the 3He pot is empty, this is the temperature it will drift towards

    def in_state(self, dt):
        device = self._context

        rate = 0.1

        device.temperature = approaches.linear(device.temperature, He3PotEmptyState.DRIFT_TOWARDS, rate, dt)
