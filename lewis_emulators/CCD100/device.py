from lewis.devices import StateMachineDevice
from lewis.core import approaches
from states import DefaultState
from collections import OrderedDict


class SimulatedCCD100(StateMachineDevice):

    def _initialize_data(self):
        self.address = "a"
        self.setpoint = 0.00
        self.units = ""
        self.setpoint_mode = 1
        self.current_reading = 0
        self.speed = 1

        # When the device is in an error state it can respond with junk
        self.is_giving_errors = True
        self.out_error = "}{<7f>w"
        self.out_terminator_in_error = ""

    def simulate(self, dt):
        self.current_reading = approaches.linear(self.current_reading, self.setpoint, self.speed, dt)

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])
