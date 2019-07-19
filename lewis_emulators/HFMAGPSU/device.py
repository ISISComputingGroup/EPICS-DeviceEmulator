from datetime import datetime

from lewis.devices import StateMachineDevice
from collections import OrderedDict
from states import DefaultInitState, HoldingState, TrippedState, RampingState


class SimulatedHFMAGPSU(StateMachineDevice):

    def _initialize_data(self):
        # field constant (load line gradient)
        self.constant = 0.029

        # targets
        self.max_target = 10
        self.mid_target = 0.0
        self.prev_target = 0.0
        self.zero_target = 0.0
        self.at_target = False

        # ramp
        self.ramp_target = "ZERO"
        self.ramp_rate = 0.5

        # paused
        self.is_paused = True

        # output
        self.output = 0.0
        self.is_output_mode_tesla = True
        self.direction = '+'

        # heater
        self.is_heater_on = True
        self.heater_value = 0.0

        # quenched
        self.is_quenched = False

        # external trip
        self.is_xtripped = False

        # PSU voltage limit
        self.limit = 5.0

        # log message
        self.log_message = "this is the initial log message"

    def _get_state_handlers(self):
        return {
            'init': DefaultInitState(),
            'holding': HoldingState(),
            'tripped': TrippedState(),
            'ramping': RampingState(),
        }

    def _get_initial_state(self):
        return 'init'

    def _get_transition_handlers(self):

        return OrderedDict([
            (('init', 'ramping'), lambda: not self.at_target and not self.is_paused),
            (('ramping', 'holding'), lambda: self.is_paused or self.at_target),
            (('ramping', 'tripped'), lambda: self.is_quenched or self.is_xtripped),
            (('holding', 'ramping'), lambda: not self.at_target and not self.is_paused),
        ])

    # Utilities

    def timestamp_str(self):
        return datetime.now().strftime('%H:%M:%S')

    def switch_mode(self, mode):
        if mode == "TESLA":
            self.output *= self.constant
            self.max_target *= self.constant
            self.mid_target *= self.constant
            self.is_output_mode_tesla = True
        elif mode == "AMPS":
            self.output /= self.constant
            self.max_target /= self.constant
            self.mid_target /= self.constant
            self.is_output_mode_tesla = False

    def check_is_at_target(self):
        if self.output == self.ramp_target_value():
            self.at_target = True
        else:
            self.at_target = False

    def ramp_target_value(self):
        if self.ramp_target == "MID":
            return self.mid_target
        elif self.ramp_target == "MAX":
            return self.max_target
        elif self.ramp_target == "ZERO":
            return self.zero_target
        else:
            raise AssertionError("Invalid arg received")
