from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedWbvalve(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.wb_position = 1
        self.connected = True

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def reset(self):
        self._initialize_data()
