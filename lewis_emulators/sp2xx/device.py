from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from enum import Enum


class RunStatus(Enum):
    Stopped = 0
    Infusing = 1
    Withdrawing = 2



class SimulatedSp2XX(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.running_status = RunStatus.Stopped
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

    def set_running_status_via_the_back_door(self, status):
        """
        Sets running direction as an Enum to infusion or withdrawing. Called only via the backdoor.
        Args:
            direction: "infusion" or "withdrawing".

        Returns:
            None
        """
        self.running_status = RunStatus[status]

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


