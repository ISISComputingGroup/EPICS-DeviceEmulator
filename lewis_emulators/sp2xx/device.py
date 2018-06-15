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


class SimulatedSp2XX(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self._running_status = RunStatus.Stopped
        self._direction = Direction.Infusing
        self._running = False
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

    @property
    def running_status(self):
        """
        Returns the running status of the device
        """
        return self._running_status

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


