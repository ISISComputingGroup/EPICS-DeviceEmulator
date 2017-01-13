from utilities import format_value
from random import uniform
from collections import OrderedDict
from states import DefaultInitState, DefaultRunningState
from lewis.devices import StateMachineDevice


class SimulatedKeithley2400(StateMachineDevice):

    INITIAL_VALUE = 10.0

    def _initialize_data(self):
        self.serial_command_mode = True
        self._current = SimulatedKeithley2400.INITIAL_VALUE
        self._voltage = SimulatedKeithley2400.INITIAL_VALUE
        self._resistance = SimulatedKeithley2400.INITIAL_VALUE
        self._output_mode_on = True

    def _get_state_handlers(self):
        return {
            'init': DefaultInitState(),
            'running': DefaultRunningState(),
        }

    def _get_initial_state(self):
        return 'init'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('init', 'running'), lambda: self.serial_command_mode),
        ])

    def _get_output(self, value, as_string):
        return format_value(value if self._output_mode_on else 0.0, as_string)
        
    def get_voltage(self, as_string=False):
        return self._get_output(self._voltage, as_string)
        
    def get_current(self, as_string=False):
        return self._get_output(self._current, as_string)
        
    def get_resistance(self, as_string=False):
        return self._get_output(self._resistance, as_string)

    def set_current(self, value):
        self._current = value

    def set_voltage(self, value):
        self._voltage = value

    def set_resistance(self, value):
        self._resistance = value

    def reset(self):
        self._resistance = SimulatedKeithley2400.INITIAL_VALUE
        self._current = SimulatedKeithley2400.INITIAL_VALUE
        self._voltage = SimulatedKeithley2400.INITIAL_VALUE

    def set_output_on(self, is_on):
        self._output_mode_on = is_on

    def output_is_on(self):
        return self._output_mode_on

    def update(self, dt):
        def update_value(value):
            return abs(value + uniform(-1,1)*dt)
        self._current = update_value(self._current)
        self._voltage = update_value(self._voltage)
        self._resistance = update_value(self._resistance)