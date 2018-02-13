from lewis.core.statemachine import State
from lewis.core import approaches
from .channel import Channel


class DefaultState(State):

    def in_state(self, dt):
        for channel_number in self._context.channels.keys():
            channel = self._context.channels[channel_number]
            channel.trigger_auto_fill(self._context.cycle)
            if self._context.cycle:
                target = 100.0 if channel.is_filling() else 0.0
                rate = -Channel.GAS_USE_RATE
                if channel.is_filling():
                    rate += Channel.FAST_FILL_RATE if channel.is_fill_rate_fast() else Channel.SLOW_FILL_RATE
                channel.level = approaches.linear(channel.level, target, abs(rate), dt)
