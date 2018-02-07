from lewis.core.statemachine import State
from lewis.core import approaches
from .channel import Channel


class DefaultState(State):

    def in_state(self, dt):
        for channel_number in self._context.channels.keys():
            channel = self._context.channels[channel_number]
            target = 100.0 if channel.is_fill_rate_fast() else 0.0
            channel.level = approaches.linear(channel.level, target, Channel.FILL_RATE, dt)
            print("Channel {}: level - {}, fill rate - {}".format(
                channel_number, channel.get_level(), channel.is_fill_rate_fast()
            ))
