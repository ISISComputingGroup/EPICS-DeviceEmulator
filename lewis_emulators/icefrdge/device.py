from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedIceFridge(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.auto_temp_setpoint = 0
        self.manual_temp_setpoint = 0
        self.vti_temp1 = 0
        self.vti_temp2 = 0
        self.vti_temp3 = 0
        self.vti_temp4 = 0
        self.vti_loop1_temp_setpoint = 0
        self.vti_loop2_temp_setpoint = 0
        self.vti_loop1_proportional = 0
        self.vti_loop2_proportional = 0
        self.vti_loop1_integral = 0
        self.vti_loop2_integral = 0

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])
