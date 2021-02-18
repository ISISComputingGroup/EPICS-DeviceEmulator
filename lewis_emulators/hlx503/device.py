from collections import OrderedDict
from typing import Dict, Optional
from contextlib import contextmanager
from lewis.core.logging import has_log

from lewis.devices import StateMachineDevice
from .states import DefaultState

# Must match those in test
itc_names = ["1KPOT", "HE3POT_LOWT", "HE3POT_HIGHT", "SORB"]
isobus_addresses = {f"{name}_ISOBUS": i for i, name in enumerate(itc_names)}
channels = {f"{name}_CHANNEL": i for i, name in enumerate(itc_names)}
versions = {"1KPOT_VERSION": 502, "HE3POT_LOWT_VERSION": 503, "HE3POT_HIGHT_VERSION": 503, "SORB_VERSION": 601}
isobus_addresses_and_channels_zip = zip(isobus_addresses.values(), channels.values(), versions.values())
itc_zip = zip(itc_names, isobus_addresses.values(), channels.values())


class SimulatedITC503:
    """
    Simulated ITC503 for the HLX503.
    """

    def __init__(self, channel: int, version: int):
        self.version: int = version
        self.channel: int = channel
        self.temp: float = 0.0
        self.reset_status()

    def reset_status(self):
        self.status: int = 0
        self.autoheat: int = 0
        self.autoneedlevalve: int = 0
        self.initneedlevalve: int = 0
        self.remote: int = 0
        self.locked: int = 0
        self.sweeping: int = 0
        self.ctrlchannel: Optional[int] = None
        self.autopid: Optional[bool] = None
        self.tuning: Optional[bool] = None

    def set_autoheat(self, autoheat: bool):
        self.autoheat = 1 if autoheat else 0

    def set_autoneedlevalve(self, autoneedlevalve: bool):
        if self.version != 601:
            self.autoneedlevalve = 2 if autoneedlevalve else 0

    def set_initneedlevalve(self, initneedlevalve: bool):
        self.initneedlevalve = 4 if initneedlevalve else 0

    def set_remote(self, remote: bool):
        self.remote = 1 if remote else 0

    def set_locked(self, locked: bool):
        self.locked = 0 if locked else 2

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

    def get_status(self):
        mode = self.autoheat + self.autoneedlevalve + self.initneedlevalve
        control = self.remote + self.locked
        status_string = f"X{self.status}A{mode}C{control}S{self.sweeping}"
        if self.ctrlchannel is not None:
            status_string += f"H{self.ctrlchannel}"
        if self.autopid is not None:
            status_string += f"L{int(self.autopid)}"
        if self.tuning is not None:
            status_string += f"N{int(self.tuning)}"
        return status_string


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
            isobus_address: SimulatedITC503(channel, version) for isobus_address, channel, version in isobus_addresses_and_channels_zip
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

    def get_temp(self, isobus_address: int, channel: int) -> float:
        return self.itc503s[isobus_address].get_temp(channel)

    def set_temp(self, isobus_address: int, channel: int, temp: float):
        self.itc503s[isobus_address].set_temp(channel, temp)

    def get_status(self, isobus_address: int) -> str:
        return self.itc503s[isobus_address].get_status()

    def set_status(self, isobus_address: int, status: int):
        self.itc503s[isobus_address].status = status

    def set_autoheat(self, isobus_address: int, autoheat: bool):
        self.itc503s[isobus_address].set_autoheat(autoheat)

    def set_autoneedlevalve(self, isobus_address: int, autoneedlevalve: bool):
        self.itc503s[isobus_address].set_autoneedlevalve(autoneedlevalve)

    def set_initneedlevalve(self, isobus_address: int, initneedlevalve: bool):
        self.itc503s[isobus_address].set_initneedlevalve(initneedlevalve)

    def set_remote(self, isobus_address: int, remote: bool):
        self.itc503s[isobus_address].set_remote(remote)

    def set_locked(self, isobus_address: int, locked: bool):
        self.itc503s[isobus_address].set_locked(locked)

    def set_sweeping(self, isobus_address: int, sweeping: int):
        self.itc503s[isobus_address].sweeping = sweeping

    def set_ctrlchannel(self, isobus_address: int, ctrlchannel: Optional[int]):
        self.itc503s[isobus_address].ctrlchannel = ctrlchannel

    def set_autopid(self, isobus_address: int, autopid: Optional[bool]):
        self.itc503s[isobus_address].autopid = autopid

    def set_tuning(self, isobus_address: int, tuning: Optional[bool]):
        self.itc503s[isobus_address].tuning = tuning

    def reset_status(self, isobus_address: int):
        self.itc503s[isobus_address].reset_status()
