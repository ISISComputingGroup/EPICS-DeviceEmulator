from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from interfaces.stream_interface import Modes


class SimulatedKeylkg(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.input_correct = True

        self.mode = Modes.MEASURE

        self.output1_offset = 0.0
        self.output2_offset = 0.0
        self.output1_raw_value = 0.0
        self.output2_raw_value = 0.0

        self.head1_measurement_mode = 0
        self.head1_measurement_mode = 0

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
