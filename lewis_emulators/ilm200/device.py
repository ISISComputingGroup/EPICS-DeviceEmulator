from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from lewis.core.logging import has_log
from .channel import Channel


@has_log
class SimulatedIlm200(StateMachineDevice):

    LOW_LEVEL = 10.0

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.channels = {1: Channel(Channel.NITROGEN), 2: Channel(Channel.HELIUM), 3: Channel(Channel.HELIUM_CONT)}
        self.cycle = True  # Whether the device will continuously cycle through fill states

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def get_level(self, channel):
        return self.channels[channel].get_level()

    def is_fill_rate_fast(self, channel):
        return self.channels[channel].is_fill_rate_fast

    def set_fill_rate(self, channel, fast):
        self.fast_fill_rate = self.channels[channel].set_fill_rate(fast)

    def get_cryo_type(self, channel):
        return self.channels[channel].get_cryo_type()

    def set_level(self, channel, level):
        self.channels[channel].level = level

    def set_helium_current(self, channel, is_on):
        self.channels[channel].set_helium_current(is_on)
