from lewis.core import approaches
from lewis.core.statemachine import State


class DefaultState(State):

    def in_state(self, dt):
        device = self._context

        rate = 10

        for channel in device.magic_box.channels:
            channel.temperature = approaches.linear(channel.temperature, channel.temperature_sp, rate, dt)
