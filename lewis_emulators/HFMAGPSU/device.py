from lewis.devices import StateMachineDevice
from collections import OrderedDict
from states import DefaultInitState, DefaultStartedState, DefaultStoppedState


class SimulatedHFMAGPSU(StateMachineDevice):

    def _initialize_data(self):
        self._is_output_mode_tesla = True
        self._is_heater_on = True
        self._is_paused = True
        self._output = 0.0
        self._direction = '+'
        self._ramp_target = 'MID'
        self._heater_value = 0.0
        self._max_target = 34.92
        self._mid_target = 0.0
        self._ramp_rate = 0.5
        self._limit = 5.0
        self._log_message = "this is the initial log message"
        self._error_message = "this is the initial error message"
        self._constant = 0.00029
        self._zero_target = 0.0
        self._mid_final_target = 0

        self.ready = True

    def _get_state_handlers(self):
        return {
            'init': DefaultInitState(),
            'not_ramping': DefaultStoppedState(),
            'ramping': DefaultStartedState(),
        }

    def _get_initial_state(self):
        return 'init'

    def _get_transition_handlers(self):

        return OrderedDict([
            (('init', 'not_ramping'), lambda: self.ready),
            (('not_ramping', 'ramping'), lambda: not self._is_paused),
            (('ramping', 'not_ramping'), lambda: self._is_paused),
        ])

    @property
    def direction(self):
        return self._direction

    @property
    def is_output_mode_tesla(self):
        return self._is_output_mode_tesla

    @property
    def output(self):
        return self._output

    @property
    def ramp_target(self):
        return self._ramp_target

    @property
    def is_heater_on(self):
        return self._is_heater_on

    @property
    def heater_value(self):
        return self._heater_value

    @property
    def max_target(self):
        return float(self._max_target)

    @property
    def mid_target(self):
        return float(self._mid_target)

    @property
    def ramp_rate(self):
        return self._ramp_rate

    @property
    def is_paused(self):
        return self._is_paused

    @property
    def limit(self):
        return self._limit

    @property
    def log_message(self):
        return self._log_message

    @property
    def error_message(self):
        return self._error_message

    @property
    def constant(self):
        return float(self._constant)

    @property
    def zero_value(self):
        return self._zero_target

    @property
    def mid_final_target(self):
        return self._mid_final_target

    @direction.setter
    def direction(self, d):
        self._direction = d

    @is_output_mode_tesla.setter
    def is_output_mode_tesla(self, om):
        self._is_output_mode_tesla = om

    @ramp_target.setter
    def ramp_target(self, rt):
        self._ramp_target = rt

    @is_heater_on.setter
    def is_heater_on(self, hs):
        self._is_heater_on = hs

    @heater_value.setter
    def heater_value(self, hv):
        self._heater_value = hv

    @max_target.setter
    def max_target(self, mt):
        self._max_target = mt

    @mid_target.setter
    def mid_target(self, mt):
        self._mid_target = mt

    @ramp_rate.setter
    def ramp_rate(self, rate):
        self._ramp_rate = rate

    @is_paused.setter
    def is_paused(self, p):
        self._is_paused = p

    @limit.setter
    def limit(self, lim):
        self._limit = lim

    @log_message.setter
    def log_message(self, lm):
        self._log_message = lm

    @error_message.setter
    def error_message(self, em):
        self._error_message = em

    @output.setter
    def output(self, op):
        self._output = op

    @constant.setter
    def constant(self, cons):
        self._constant = cons

    @zero_value.setter
    def zero_value(self, zv):
        self._zero_value = zv

    @mid_final_target.setter
    def mid_final_target(self, mft):
        self._mid_final_target = mft
