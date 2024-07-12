from collections import OrderedDict
from threading import Timer

from .states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedPt2025(StateMachineDevice):
    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.status = ""
        self.data = ""

    def reset_values(self):
        """
        Public method that re-initializes the device's fields.
        :return: Nothing.
        """
        self._initialize_data()

    def _get_state_handlers(self):
        return {
            "default": DefaultState(),
        }

    def _get_initial_state(self):
        return "default"

    def _get_transition_handlers(self):
        return OrderedDict([])
