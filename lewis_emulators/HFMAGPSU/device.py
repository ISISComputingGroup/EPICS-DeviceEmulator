from lewis.devices import StateMachineDevice
from collections import OrderedDict
from .states import DefaultState


class SimulatedHFMAGPSU(StateMachineDevice):


    def _initialize_data(self):
        self._is_output_mode_tesla = False
        self._is_heater_on = False
        self._is_paused = False
        self._direction = 0
        self._ramp_target = 0
        self._heater_value = 1.0
        self._max_target = 5.0
        self._mid_target = 2.5
        self._ramp_rate = 10.0
        self._limit = 10
        self._log_message = "this is the initial log message"

    def _get_state_handlers(self):
        return {DefaultState.NAME: DefaultState()}

    def _get_initial_state(self):
        return DefaultState.NAME

    def _get_transition_handlers(self):
        return OrderedDict()

    @property
    def direction(self):
        return self._direction

    @property
    def is_output_mode_tesla(self):
        return self._is_output_mode_tesla

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
        return self._max_target

    @property
    def mid_target(self):
        return self._mid_target

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
