from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class SimulatedHLX503(StateMachineDevice):
    """
    Simulated ITC503/Heliox based cryogenic refrigerator.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self.connected = True

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
