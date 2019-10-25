from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class VTILoopChannel(object):
    """
    Class to represent an individual channel for controlling loops in the VTI of an ICE dilution fridge. A channel has
    a temperature setpoint, PID values and a ramp rate.
    """

    def __init__(self):
        self.vti_loop_temp_setpoint = 0
        self.vti_loop_proportional = 0
        self.vti_loop_integral = 0
        self.vti_loop_derivative = 0
        self.vti_loop_ramp_rate = 0

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

        self.vti_loop_channels = {
            "1": VTILoopChannel(),
            "2": VTILoopChannel()
        }

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])
