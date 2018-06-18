from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from enum import Enum


class RunStatus(Enum):
    Stopped = 0
    Infusing = 1
    Withdrawing = 2


class Direction(Enum):
    Infusing = 0
    Withdrawing = 1


MODES = {
    "i": "Infusion",
    "w": "Withdrawal",
    "i//w": "Infusion_Withdrawal",
    "w//i": "Withdrawal_Infusion",
    "con": "Continuous"
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
        self._direction = Direction.Infusing
        self._running = False
        self._last_error = NO_ERROR
        self._mode = MODES["i"]
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

    def start_device(self):
        """
        Starts the device running to present settings.

        Returns:
            None
        """
        self.clear_last_error()
        self._running = True
        self._running_status = RunStatus[self._direction.name]

    def stop_device(self):
        """
        Stops the device running.

        Returns:
            None
        """
        self.clear_last_error()
        self._running = False
        self._running_status = RunStatus.Stopped

    @property
    def running_status(self):
        """
        Returns the running status of the device.
        """
        self.clear_last_error()
        return self._running_status

    @property
    def mode(self):
        """
        Returns the mode the device is in.

        Returns:
            mode (Enum) the device is in.
        """
        self.clear_last_error()
        return self._mode

    def set_mode_via_the_backdoor(self, mode_symbol):
        """
        Sets the mode of the device. Only used via the backdoor.

        Args:
            mode_symbol: Symbol of the mode to be set. One of i, w, i//w, w//i, con.

        Returns:
            None
        """

        self.clear_last_error()
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
            error_type: Integer 0-7 of the error type.

        Returns:
            "\r\nE": Device error prompt.
        """
        self._last_error = ErrorType(error_name, error_value, error_alarm_severity)

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
