from collections import OrderedDict
from lewis.core.logging import has_log
from states import DefaultState
from lewis.devices import StateMachineDevice


@has_log
class SimulatedHeliox(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.temperature = 0
        self.temperature_sp = 0

    def _get_state_handlers(self):
        return {'default': DefaultState()}

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])
