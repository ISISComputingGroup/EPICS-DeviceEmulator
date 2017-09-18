from lewis.devices import StateMachineDevice
from collections import OrderedDict
from .states import DefaultState


class SimulatedHFMAGPSU(StateMachineDevice):

    def _initialize_data(self):
        self.is_output_mode_tesla = False
        self.is_heater_on = True
        self.is_paused = True
        self.output = 0
        self.direction = '-'
        self.ramp_target = 'ZERO'
        self.heater_value = 1.0
        self.max_target = 20.0
        self.mid_target = 10.0
        self.ramp_rate = 0.5
        self.limit = 10
        self.log_message = "this is the initial log message"

    def _get_state_handlers(self):
        return {DefaultState.NAME: DefaultState()}

    def _get_initial_state(self):
        return DefaultState.NAME

    def _get_transition_handlers(self):
        return OrderedDict()
