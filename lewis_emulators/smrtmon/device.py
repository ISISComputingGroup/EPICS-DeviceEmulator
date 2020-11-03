from lewis.devices import StateMachineDevice
from .states import DefaultState
from collections import OrderedDict


class SimulatedSmrtmon(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.stat1 = 0
        self.oplm1 = 0
        self.lims1 = 0

    def get_stat1(self):
        return self.stat1

    def get_oplm1(self):
        return self.oplm1

    def get_lims1(self):
        return self.lims1

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])
