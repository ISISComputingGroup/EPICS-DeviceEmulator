from collections import OrderedDict
from lewis.devices import StateMachineDevice
from .states import DefaultState
from lewis.core.logging import has_log


@has_log
class SimulatedLakeshore218(StateMachineDevice):
    """
    Simulated Lakeshore 218
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self._temps = [1] * 8

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

    def get_temp(self, number):
        return self._temps[number - 1]

    def set_temp(self, number, temperature):
        self._temps[int(number) - 1] = float(temperature)

