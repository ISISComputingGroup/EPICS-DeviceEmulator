from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedFermichopper(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.property = 5

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])

    def set_property(self, value):
        self.property = value

    def get_property(self, value):
        return self.property

