from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedFermichopper(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.last_command = "0000"

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])

    def set_last_command(self, value):
        self.last_command = value

    def get_last_command(self):
        return self.last_command

