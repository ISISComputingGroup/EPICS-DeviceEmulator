from collections import OrderedDict
from lewis.core.logging import has_log
from states import DefaultState
from lewis.devices import StateMachineDevice


class TemperatureChannel(object):
    """
    Class to represent an individual temperature channel on a Heliox fridge. e.g. He3Sorb or He4Pot channels.
    """
    def __init__(self):
        self.temperature = 0
        self.temperature_sp = 0
        self.stable = True
        self.heater_auto = True
        self.heater_percent = 0


@has_log
class SimulatedHeliox(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.temperature = 0
        self.temperature_sp = 0

        self.temperature_stable = True

        self.temperature_channels = {
            "HE3SORB": TemperatureChannel(),
            "HE4POT": TemperatureChannel(),
            "HELOW": TemperatureChannel(),
            "HEHIGH": TemperatureChannel(),
        }

    def _get_state_handlers(self):
        return {
            'default': DefaultState()
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])

    def backdoor_set_channel_temperature(self, channel, temperature):
        self.temperature_channels[channel].temperature = temperature

    def backdoor_set_channel_temperature_sp(self, channel, temperature_sp):
        self.temperature_channels[channel].temperature_sp = temperature_sp

    def backdoor_set_channel_stability(self, channel, stability):
        self.temperature_channels[channel].stable = stability

    def backdoor_set_channel_heater_auto(self, channel, heater_auto):
        self.temperature_channels[channel].heater_auto = heater_auto

    def backdoor_set_channel_heater_percent(self, channel, percent):
        self.temperature_channels[channel].heater_percent = percent
