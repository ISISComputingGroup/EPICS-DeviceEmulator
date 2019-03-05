import math
import random
import time
from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedKeylkg(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.mode = "NORMAL"
        self.out_number = 0

        self.output1_offset = 0.0
        self.output2_offset = 0.0

        self.head1_measurement_mode = 0
        self.head1_measurement_mode = 0

    @property
    def output1_value(self):
        return float(math.sin(random.randint(0, 10))) - self.output2_offset

    @property
    def output2_value(self):
        return float(math.sin(random.randint(0, 10))) - self.output2_offset

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
