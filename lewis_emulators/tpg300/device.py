from collections import OrderedDict
from lewis.devices import StateMachineDevice
from .states import DefaultState
from enum import Enum


class Units(Enum):
    mbar = 1
    Torr = 2
    Pa = 3


class SimulatedTpg300(StateMachineDevice):
    """
    Simulated TPG300.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """

        self.pressure_a1 = 0
        self.pressure_a2 = 0
        self.pressure_b1 = 0
        self.pressure_b2 = 0
        self.units = Units["mbar"]
        self.connected = True

    @staticmethod
    def _get_state_handlers():
        """
        Returns: states and their names
        """

        return {DefaultState.NAME: DefaultState()}

    @staticmethod
    def _get_initial_state():
        """
        Returns: the name of the initial state
        """
        return DefaultState.NAME

    @staticmethod
    def _get_transition_handlers():
        """
        Returns: the state transitions
        """
        return OrderedDict()

