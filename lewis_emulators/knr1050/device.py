from states import DefaultState
from lewis.devices import StateMachineDevice
from collections import OrderedDict
from enum import Enum

class SimulatedKnr1050(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True

        self.current_instrument_state = 0
        self.instrument_state = ('SYS_ST_INITIALIZING',
                                 'SYS_ST_OFF',
                                 'SYS_ST_IDLE',
                                 'SYS_ST_RUN',
                                 'SYS_ST_HOLD',
                                 'SYS_ST_PURGE',
                                 'SYS_ST_STANDBY')

        self.is_stopped = False
        self.keep_last_values = False
        self.ramp_status = False

        self.pressure_limit_low = 0
        self.pressure_limit_high = 100

        self.flow_rate = 0

        self.concentration_A = 0
        self.concentration_B = 0
        self.concentration_C = 0
        self.concentration_D = 0


    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def get_instrument_state_str(self, current_instrument_state):
        return self.instrument_state[current_instrument_state]