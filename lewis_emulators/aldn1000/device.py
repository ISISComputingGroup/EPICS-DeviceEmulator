from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedAldn1000(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.input_correct = True

        self.status = 'S'
        self.pump = 'STP'
        self.program_function = 'RAT'

        self.address = 0
        self.diameter = 0.0
        self.volume = 0.0
        self.volume_infused = 0.0
        self.volume_withdrawn = 0.0
        self.direction = 'INF'
        self.rate = 0.0
        self.units = 'UM'
        self.volume_units = 'UL'

    def reset(self):
        self._initialize_data()

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

