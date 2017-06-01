from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class SimulatedTpg26x(StateMachineDevice):
    """
    Simulated TPG26x
    """

    def _initialize_data(self):

        """

        Sets the initial state of the device

        """

        self._pressure1 = 2.0
        self._pressure2 = 3.0

    def _get_state_handlers(self):

        """

        Returns: states and their names

        """
        return {
            DefaultState.NAME: DefaultState(),
        }

    def _get_initial_state(self):
        """

        Returns: the name of the initial state

        """
        return DefaultState.NAME

    def _get_transition_handlers(self):

        """

        Returns: the state transitions

        """

        return OrderedDict([
        ])

    @property
    def pressure1(self):
        """
        Returns: the first pressure
        """
        return self._pressure1

    @pressure1.setter
    def pressure1(self, pressure):
        """
        Set the pressure for pressure 1
        :param pressure: the pressure value to set the first pressure to
        """
        self._pressure1 = pressure

    @property
    def pressure2(self):
        """
        Returns: the second pressure
        """
        return self._pressure2

    @pressure2.setter
    def pressure2(self, pressure):
        """
        Set the pressure for pressure 2
        :param pressure: the pressure value to set the second pressure to
        """
        self._pressure2 = pressure
