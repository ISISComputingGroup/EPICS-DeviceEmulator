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
        self._offset_compensation_on = False
        self._output_mode_on = True
        self._resistance_mode_auto = True
        self._remote_sensing_on = False
        self._auto_resistance_range = True

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
        return format_value((value - SimulatedKeithley2400.INITIAL_VALUE if self._offset_compensation_on else value)
                            if self._output_mode_on else 0.0,
                            as_string)
        
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

    def set_offset_compensation_on(self, is_on):
        self._offset_compensation_on = is_on

    def offset_compensation_is_on(self):
        return self._offset_compensation_on

    def update(self, dt):
        def update_value(value):
            return abs(value + uniform(-1,1)*dt)
        self._current = update_value(self._current)
        self._voltage = update_value(self._voltage)
        self._resistance = update_value(self._resistance)

    def resistance_mode_is_auto(self):
        return self._resistance_mode_auto

    def set_resistance_mode_auto(self, is_auto):
        self._resistance_mode_auto = is_auto

    def remote_sensing_is_on(self):
        return self._remote_sensing_on

    def set_remote_sensing_on(self, is_on):
        self._remote_sensing_on = is_on

    def auto_resistance_range_is_on(self):
        return self._auto_resistance_range

    def set_auto_resistance_on(self, is_on):
        self._auto_resistance_range = is_on
