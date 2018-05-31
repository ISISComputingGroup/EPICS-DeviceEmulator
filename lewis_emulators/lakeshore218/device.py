from collections import OrderedDict
from lewis.devices import StateMachineDevice
from .states import DefaultState

class SimulatedLakeshore218(StateMachineDevice):
    """
    Simulated Lakeshore 218
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self._temp_1 = 1.0

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
