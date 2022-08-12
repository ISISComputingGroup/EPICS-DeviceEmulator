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
class FunctionsSet(Enum):
    FS1 = 0
    FS2 = 1
    FS3 = 2
    FS4 = 3
    FSA = 4
    FSB = 5


@unique
class FunctionsRead(Enum):
    F1 = 0
    F2 = 1
    F3 = 2
    F4 = 3
    FA = 4
    FB = 5


@unique
class ReadState(Enum):
    A1 = "a1"
    A2 = "a2"
    B1 = "b1"
    B2 = "b2"
    UNI = 0
    UNI1 = 1
    UNI2 = 2
    UNI3 = 3
    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"
    FA = "FA"
    FB = "FB"
    FS1 = "FS1"
    FS2 = "FS2"
    FS3 = "FS3"
    FS4 = "FS4"
    FSA = "FSA"
    FSB = "FSB"
    SPS = "SPS"




class CircuitAssignment:
    """
    This object represents settings for a circuit in the device.
        these settings are: high_threshold(float), high_exponent(int),
        low_threshold(float), low_exponent(int), circuit_assignment(1|2|2|4|A|B)
    """

    def __init__(self, high_threshold=0.0, high_exponent=0, low_threshold=0.0, low_exponent=0, circuit_assignment=1):
        """
        Default constructor.
        """
        self.high_threshold = high_threshold
        self.high_exponent = high_exponent
        self.low_threshold = low_threshold
        self.low_exponent = low_exponent
        self.circuit_assignment = circuit_assignment


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
        self.__units = Units["mbar"]
        self.__connected = None
        self.__readstate = None
        self.__switching_function_to_set = CircuitAssignment()
        self.__switching_functions = [CircuitAssignment(), CircuitAssignment(), CircuitAssignment(),
                                      CircuitAssignment(), CircuitAssignment(), CircuitAssignment()]
        self.__switching_functions_status = [0, 0, 0, 0, 0, 0]
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
    def switching_functions_status(self):
        """
        Returns status of the switching functions.

        Returns:
            list of 6 values which can be 0 (off) or 1 (on)
        """
        return self.__switching_functions_status

    @switching_functions_status.setter
    def switching_functions_status(self, status):
        """
        Sets the status of the switching functions.

        Args:
            status: list of 6 values which can be 0 (off) or 1 (on)
        Returns:
            None
        """
        self.__switching_functions_status = status

    @property
    def switching_functions(self):
        """
        Returns the settings of a switching function

        Returns:
            list of 6 CircuitAssignment instances
        """
        return self.__switching_functions

    @switching_functions.setter
    def switching_functions(self, function_list):
        """
        Sets the status of the switching functions.

        Args:
            function_list: list of 6 CircuitAssignment instances
        Returns:
            None
        """
        self.__switching_functions = function_list

    @property
    def switching_function_to_set(self):
        """
        Returns the thresholds of the switching function that will be saved upon receiving ENQ signal.

        Returns:
            CircuitAssignment instance
        """
        return self.__switching_function_to_set

    @switching_function_to_set.setter
    def switching_function_to_set(self, function):
        """
        Sets the thresholds of the switching function that will be saved upon receiving ENQ signal.

        Args:
            function: CircuitAssignment instance
        Returns:
            None
        """
        self.__switching_function_to_set = function

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

    def backdoor_set_switching_function_status(self, status):
        """
        Sets status of switching functions. Called only via the backdoor using lewis.

        Args:
            status: list of 6 values which can be 0 (off) or 1 (on)

        Returns:
            None
        """

        self.switching_functions_status = status
