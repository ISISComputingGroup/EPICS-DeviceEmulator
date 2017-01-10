from utilities import format_value
from collections import OrderedDict
from states import DefaultInitState, DefaultRunningState
from lewis.devices import StateMachineDevice


class SimulatedVolumetricRig(StateMachineDevice):

    def _initialize_data(self):
        self.serial_command_mode = True
        self._current = 0.0
        self._voltage = 0.0
        self._resistance = 0.0

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
        
    def get_voltage(self, as_string=False):
        return format_value(self._voltage, as_string)
        
    def get_current(self, as_string=False):
        return format_value(self._current, as_string)
        
    def get_resistance(self, as_string=False):
        return format_value(self._resistance, as_string)

    def set_current(self, value):
        self._current = value

    def set_voltage(self, value):
        self._voltage = value

    def set_resistance(self, value):
        self._resistance = value

