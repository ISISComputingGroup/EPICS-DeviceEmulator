from collections import OrderedDict
from states import DefaultInitState, DefaultRunningState
from lewis.devices import StateMachineDevice


class SimulatedMk2Chopper(StateMachineDevice):

    def _initialize_data(self):
        """ Initialize all of the device's attributes """
        self.serial_command_mode = True
        self.demanded_frequency = 50

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

    def update(self, dt):
        pass

    def get_demanded_frequency(self):
        return self.demanded_frequency
