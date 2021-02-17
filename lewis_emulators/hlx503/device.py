from collections import OrderedDict
from typing import Dict
from contextlib import contextmanager
from lewis.core.logging import has_log

from lewis.devices import StateMachineDevice
from .states import DefaultState

itc_names = ["SORB", "1KPOT", "HE3POT_LOWT", "HE3POT_HIGHT"]
isobus_addresses = {f"{name}_ISOBUS": i for i, name in enumerate(itc_names)}
channels = {f"{name}_CHANNEL": i for i, name in enumerate(itc_names)}
isobus_addresses_and_channels_zip = zip(isobus_addresses.values(), channels.values())
itc_zip = zip(itc_names, isobus_addresses.values(), channels.values())


class SimulatedITC503:
    """
    Simulated ITC503 for the HLX503.
    """

    def __init__(self, channel):
        self.channel = channel
        self.temp = 1.0

    @contextmanager
    def check_channel(self, channel):
        if self.channel == channel:
            yield
        else:
            raise ValueError(f"Channel {channel} incorrect. Expected {self.channel}")

    def set_temp(self, channel, temp):
        with self.check_channel(channel):
            self.temp = temp

    def get_temp(self, channel):
        with self.check_channel(channel):
            return self.temp


@has_log
class SimulatedHLX503(StateMachineDevice):
    """
    Simulated ITC503/Heliox based cryogenic refrigerator.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self.connected = True
        self.itc503s: Dict[int, SimulatedITC503] = {
            isobus_address: SimulatedITC503(channel) for isobus_address, channel in isobus_addresses_and_channels_zip
        }

    def _get_state_handlers(self):
        """
        Returns: states and their names
        """
        return {DefaultState.NAME: DefaultState()}

    def _get_initial_state(self):
        """
        Returns: the name of the initial state
        """
        return DefaultState.NAME

    def _get_transition_handlers(self):
        """
        Returns: the state transitions
        """
        return OrderedDict()

    def get_temp(self, isobus_address, channel):
        temp = self.itc503s[isobus_address].get_temp(channel)
        self.log.info(f"GET: {temp}")
        return temp

    def set_temp(self, isobus_address, channel, temp):
        self.log.info(f"SET: {temp}")
        self.itc503s[isobus_address].set_temp(channel, temp)
