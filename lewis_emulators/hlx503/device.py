from collections import OrderedDict
from typing import Dict, Optional
from contextlib import contextmanager
from dataclasses import dataclass

from lewis.core.logging import has_log
from lewis.devices import StateMachineDevice
from .states import DefaultState


@dataclass
class ITC:
    name: str
    channel : int
    isobus_address: int


# Must match those in test
itcs = [
    ITC("1KPOT", 1, 1), ITC("HE3POT_LOWT", 2, 2),
    ITC("HE3POT_HIGHT", 3, 3), ITC("SORB", 4, 4)
]


class SimulatedITC503:
    """
    Simulated ITC503 for the HLX503.
    """

    def __init__(self, channel: int):
        self.channel: int = channel
        self.reset_status()

    def reset_status(self):
        self.temp: float = 0.0
        self.temp_sp: float = 0.0
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
        self.proportional: float = 0.0
        self.integral: float = 0.0
        self.derivative: float = 0.0
        self.heater_output: float = 0.0

    def set_autoheat(self, autoheat: bool):
        self.autoheat = 1 if autoheat else 0

    def set_autoneedlevalve(self, autoneedlevalve: bool):
        self.autoneedlevalve = 2 if autoneedlevalve else 0

    def set_autopid(self, autopid: Optional[bool]):
        self.autopid = autopid

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

    def set_temp(self, temp):
        self.temp_sp = temp
        self.temp = temp

    def get_temp(self, channel) -> float:
        if channel == 0:
            return self.temp_sp
        else:
            with self.check_channel(channel):
                return self.temp

    def get_status(self) -> str:
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
            itc.isobus_address: SimulatedITC503(itc.channel) for itc in itcs
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

    def set_temp(self, isobus_address: int, temp: float):
        self.itc503s[isobus_address].set_temp(temp)

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
        self.itc503s[isobus_address].set_autopid(autopid)

    def set_tuning(self, isobus_address: int, tuning: Optional[bool]):
        self.itc503s[isobus_address].tuning = tuning

    def reset_status(self, isobus_address: int):
        self.itc503s[isobus_address].reset_status()

    def set_proportional(self, isobus_address: int, proportional: float):
        self.itc503s[isobus_address].proportional = proportional

    def set_integral(self, isobus_address: int, integral: float):
        self.itc503s[isobus_address].integral = integral

    def set_derivative(self, isobus_address: int, derivative: float):
        self.itc503s[isobus_address].derivative = derivative

    def get_proportional(self, isobus_address: int) -> float:
        return self.itc503s[isobus_address].proportional

    def get_integral(self, isobus_address: int) -> float:
        return self.itc503s[isobus_address].integral

    def get_derivative(self, isobus_address: int) -> float:
        return self.itc503s[isobus_address].derivative

    def set_heater_output(self, isobus_address: int, heater_output: float):
        self.itc503s[isobus_address].heater_output = heater_output

    def get_heater_output(self, isobus_address: int) -> float:
        return self.itc503s[isobus_address].heater_output
