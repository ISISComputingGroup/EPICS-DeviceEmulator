from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class SimulatedTpg300(StateMachineDevice):
    """
    Simulated TPG300.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """

        self._pressure_A1 = 1.0
        self._pressure_A2 = 2.0
        self._pressure_B1 = 3.0
        self._pressure_B2 = 4.0
        self._units = 0

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

    @property
    def pressure_A1(self):
        """
        Returns: Pressure A1
        """

        return self._pressure_A1

    @pressure_A1.setter
    def pressure_A1(self, pressure):
        """
        Sets the pressure for pressure A1

        :param pressure: The pressure value to set A1 to
        """

        self._pressure_A1 = pressure

    @property
    def pressure_A2(self):
        """
        Returns: Pressure A2
        """

        return self._pressure_A2

    @pressure_A2.setter
    def pressure_A2(self, pressure):
        """
        Sets the pressure for pressure A2

        :param pressure: The pressure value to set A2 to
        """

        self._pressure_A2 = pressure

    @property
    def pressure_B1(self):
        """
        Returns: Pressure B1
        """

        return self._pressure_B1

    @pressure_B1.setter
    def pressure_B1(self, pressure):
        """
        Sets the pressure for pressure B1

        :param pressure: The pressure value to set B1 to
        """

        self._pressure_B1 = pressure

    @property
    def pressure_B2(self):
        """
        Returns: Pressure B2
        """

        return self._pressure_B2

    @pressure_B2.setter
    def pressure_B2(self, pressure):
        """
        Sets the pressure for pressure B2

        :param pressure: The pressure value to set B2 to
        """

        self._pressure_B2 = pressure

    @property
    def units(self):
        """
        Returns: the units for TPG300
        """
        return self._units

    @units.setter
    def units(self, units):
        """
        Set the units for TPG300

        Args:
            units (string): The units to set the device to.
        """
        self._units = units
