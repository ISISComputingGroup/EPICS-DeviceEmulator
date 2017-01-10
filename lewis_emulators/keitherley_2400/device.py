from utilities import format
from collections import OrderedDict
from lewis.devices import StateMachineDevice


class SimulatedVolumetricRig(StateMachineDevice):

    def _initialize_data(self):
        self.serial_command_mode = True
        self._current = 1.111
        self._voltage = 2.222
        self._resistance = 3.333

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
        return format(self._voltage, as_string)
        
    def get_current(self, as_string=False):
        return format(self._current, as_string)
        
    def get_resistance(self, as_string=False):
        return format(self._resistance, as_string)
