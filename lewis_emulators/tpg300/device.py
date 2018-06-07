from collections import OrderedDict
from lewis.devices import StateMachineDevice
from .states import DefaultState
from enum import Enum, unique


@unique
class Units(Enum):
    mbar = 1
    Torr = 2
    Pa = 3


@unique
class ReadState(Enum):
    A1 = "a1"
    A2 = "a2"
    B1 = "b1"
    B2 = "b2"
    UNI = 0
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

        self.__pressure_a1 = 0.0
        self.__pressure_a2 = 0.0
        self.__pressure_b1 = 0.0
        self.__pressure_b2 = 0.0
        self.__units = None
        self.__connected = None
        self.__readstate = None

        self.connect()

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
        Returns the value of the A1 pressure sensor.

        Returns:
            float: Pressure A1 value.
        """
        return self.__pressure_a1

    @pressure_a1.setter
    def pressure_a1(self, value):
        """
        Sets the A1 pressure sensor.

        Args:
            value: Value to set A1 pressure sensor to.
        Returns:
            None
        """
        self.__pressure_a1 = value

    @property
    def pressure_a2(self):
        """
        Returns the value of the A2 pressure sensor.

        Returns:
            float: Pressure A1 value.
        """
        return self.__pressure_a2

    @pressure_a2.setter
    def pressure_a2(self, value):
        """
        Sets the B1 pressure sensor.

        Args:
            value: Value to set B1 pressure sensor to.
        Returns:
            None
        """
        self.__pressure_a2 = value

    @property
    def pressure_b1(self):
        """
        Returns the value of the A2 pressure sensor.

        Returns:
            float: Pressure A1 value.
        """
        return self.__pressure_b1

    @pressure_b1.setter
    def pressure_b1(self, value):
        """
        Sets the B1 pressure sensor.

        Args:
            value: Value to set B1 pressure sensor to.
        Returns:
            None
        """
        self.__pressure_b1 = value

    @property
    def pressure_b2(self):
        """
        Returns the value of the B2 pressure sensor.

        Returns:
            float: Pressure B2 value.
        """
        return self.__pressure_b2

    @pressure_b2.setter
    def pressure_b2(self, value):
        """
        Sets the B2 pressure sensor.

        Args:
            value: Value to set B2 pressure sensor to.
        Returns:
            None
        """
        self.__pressure_b2 = value

    @property
    def units(self):
        """
        Returns units currently set of the device.

        Returns:
            unit (Enum member): Enum member of Units Enum.
        """
        return self.__units

    @units.setter
    def units(self, units):
        """
        Sets the devices units.

        Args:
            units: Enum member of Units.
        Returns:
            None
        """
        self.__units = units

    @property
    def connected(self):
        """
        Returns the current connected state.

        Returns:
            bool: Current connected state.
        """
        return self.__connected

    def connect(self):
        """
        Connects the device.

        Returns:
            None
        """

        self.__connected = True

    def disconnect(self):
        """
        Disconnects the device.

        Returns:
            None
        """

        self.__connected = False

    @property
    def readstate(self):
        """
        Returns the readstate for the device

        Returns:
            Enum: Readstate of the device.
        """
        return self.__readstate

    @readstate.setter
    def readstate(self, state):
        """
        Sets the readstate of the device

        Args:
            state: Enum readstate of the device to be set

        Returns:
            None
        """
        self.__readstate = state

    def backdoor_set_unit(self, unit):
        """
        Sets unit on device. Called only via the backdoor using lewis.

        Args:
            unit: integer 1, 2, or 3

        Returns:
            None
        """

        self.units = Units(unit)


