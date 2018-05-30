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

        self._pressure_a1 = 1.0
        self._pressure_a2 = 2.0
        self._pressure_b1 = 3.0
        self._pressure_b2 = 4.0
        self._units = 1
        
        self._connected = True

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

    @property
    def pressure_a1(self):
        """
        Returns: Pressure a1
        """

        return self._pressure_a1

    @pressure_a1.setter
    def pressure_a1(self, pressure):
        """
        Sets the pressure for pressure a1

        :param pressure: The pressure value to set A1 to
        """

        self._pressure_a1 = pressure

    @property
    def pressure_a2(self):
        """
        Returns: Pressure A2
        """

        return self._pressure_a2

    @pressure_a2.setter
    def pressure_a2(self, pressure):
        """
        Sets the pressure for pressure A2

        :param pressure: The pressure value to set A2 to
        """

        self._pressure_a2 = pressure

    @property
    def pressure_b1(self):
        """
        Returns: Pressure B1
        """

        return self._pressure_b1

    @pressure_b1.setter
    def pressure_b1(self, pressure):
        """
        Sets the pressure for pressure B1

        :param pressure: The pressure value to set B1 to
        """

        self._pressure_b1 = pressure

    @property
    def pressure_b2(self):
        """
        Returns: Pressure B2
        """

        return self._pressure_b2

    @pressure_b2.setter
    def pressure_b2(self, pressure):
        """
        Sets the pressure for pressure B2

        :param pressure: The pressure value to set B2 to
        """

        self._pressure_b2 = pressure

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

    @property
    def connected(self):
        """
        Returns:
            bool: True if emulator is running in connected mode.
                False if emulator is running in disconnected mode.
        """
        return self._connected

    @connected.setter
    def connected(self, connected):
        """
        Set the (connected|disconnected) status for the emulator

        Args:
            connected: bool
        """
        self._connected = connected
