from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from enum import Enum


class RunStatus(Enum):
    Stopped = 0
    Infusing = 1
    Withdrawing = 2


class Direction(Enum):
    I = 0
    W = 1


class Mode(object):
    """
    Operation mode for the device.

    Attributes:
        set_symbol (string): Symbol for setting the mode
        response (string): Response to a query for the mode.
        name: Description of the mode.
    """
    def __init__(self, set_symbol, response, name):
        self.set_symbol = set_symbol
        self.response = response
        self.name = name


infusion = Mode("i", "I", "Infusion")
withdrawal = Mode("w", "W", "Withdrawal")
infusion_withdrawal = Mode("i/w", "IW", "Infusion/Withdrawal")
withdrawal_infusion = Mode("w/i", "WI", "Withdrawal/Infusion")
continuous = Mode("con", "CON", "Continuous")

MODES = {
    "i": infusion,
    "w": withdrawal,
    "i/w": infusion_withdrawal,
    "w/i": withdrawal_infusion,
    "con": continuous
}


class ErrorType(object):
    """
    Error Type.

    Attributes:
        name: String name of the error
        value: integer value of the error
        alarm_severity: Alarm severity of the error
    """
    def __init__(self, name, value, alarm_severity):
        self.name = name
        self.value = value
        self.alarm_severity = alarm_severity


NO_ERROR = ErrorType("No error", 0, "NO_ALARM")


class SimulatedSp2XX(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self._running_status = RunStatus.Stopped
        self._direction = Direction.I
        self._running = False
        self._last_error = NO_ERROR
        self._mode = infusion
        self.connect()

    @staticmethod
    def _get_state_handlers():
        return {
            'default': DefaultState(),
        }

    @staticmethod
    def _get_initial_state():
        return 'default'

    @staticmethod
    def _get_transition_handlers():
        return OrderedDict([
        ])

    @property
    def running(self):
        """
        Returns True if the device is running and False otherwise.
        """
        return self._running

    @property
    def direction(self):
        """
        Returns the direction the pump is set to.
        """
        return self._direction

    def set_direction_via_the_backdoor(self, direction):
        """
        Sets the direction via the backdoor. Only called using lewis via the backdoor.

        Args:
            direction: Infusion or Withdrawal.

        Returns:
            None
        """
        self._direction = Direction[direction]

    def start_device(self):
        """
        Starts the device running to present settings.

        Returns:
            None
        """

        self._running = True
        self._running_status = RunStatus[self._direction.name]

    def stop_device(self):
        """
        Stops the device running.

        Returns:
            None
        """

        self._running = False
        self._running_status = RunStatus.Stopped

    @property
    def running_status(self):
        """
        Returns the running status of the device.
        """

        return self._running_status

    @property
    def mode(self):
        """
        Returns the mode the device is in.

        Returns:
            mode (Enum) the device is in.
        """

        return self._mode

    def set_mode(self, mode_symbol):
        """
        Sets the mode of the device.

        Args:
            mode_symbol: one of i, w, w//i, i//w, con.

        Returns:
            None
        """

        self._mode = MODES[mode_symbol]

    def set_mode_via_the_backdoor(self, mode_symbol):
        """
        Sets the mode of the device. Only used via the backdoor.

        Args:
            mode_symbol: Symbol of the mode to be set. One of i, w, i//w, w//i, con.

        Returns:
            None
        """

        self._mode = MODES[mode_symbol]

    @property
    def last_error(self):
        """
         Returns the last error type.

        """
        return self._last_error

    def throw_error_via_the_backdoor(self, error_name, error_value, error_alarm_severity):
        """
        Throws an error of type error_type. Set only via the backdoor

        Args:
            error_name: Name of the error to throw.
            error_value: Integer value of error.
            error_alarm_severity: Alarm severity.

        Returns:
            "\r\nE": Device error prompt.
        """
        new_error = ErrorType(error_name, error_value, error_alarm_severity)
        self._last_error = new_error

    def clear_last_error(self):
        """
        Clears the last error.

        Returns:
            None.
        """
        self._last_error = NO_ERROR

    @property
    def connected(self):
        """
        Returns True if the device is connected and False if disconnected.
        """
        return self._connected

    def connect(self):
        """
        Connects the device.

        Returns:
            None
        """
        self._connected = True

    def discconnect(self):
        """
        Disconnects the device.

        Returns:
            None
        """
        self._connected = False
