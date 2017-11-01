from collections import OrderedDict

from lewis.core.statemachine import State
from lewis.devices import StateMachineDevice


class SimulatedSkfMb350Chopper(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

    def _get_state_handlers(self):
        return {
            'init': State(),
        }

    def _get_initial_state(self):
        return 'init'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('init', 'stopped'), lambda: False),
        ])
