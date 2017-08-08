from collections import OrderedDict
from states import DormantState, GasFlowState, PumpPurgeFillState, PumpState, SingleShotState
from lewis.devices import StateMachineDevice


class SimulatedIeg(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.unique_id = 123

        self.gas_valve_open = False
        self.buffer_valve_open = False
        self.pump_valve_open = False

        self.operatingmode = 0

        self.sample_pressure_high_limit = 100
        self.sample_pressure_low_limit = 10
        self.sample_pressure = 0

        self.error = 0

        self.buffer_pressure_high = True

    def _get_state_handlers(self):
        return {
            'dormant': DormantState(),
            'gas_flow': GasFlowState(),
            'pump_purge_fill': PumpPurgeFillState(),
            'pump': PumpState(),
            'single_shot': SingleShotState(),
        }

    def _get_initial_state(self):
        return 'dormant'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('dormant', 'pump_purge_fill'), lambda: self.operatingmode == 1),
            (('pump_purge_fill', 'dormant'), lambda: self.operatingmode != 1),

            (('dormant', 'pump'), lambda: self.operatingmode == 2),
            (('pump', 'dormant'), lambda: self.operatingmode != 2),

            (('dormant', 'gas_flow'), lambda: self.operatingmode == 3),
            (('gas_flow', 'dormant'), lambda: self.operatingmode != 3),

            (('dormant', 'single_shot'), lambda: self.operatingmode == 4),
            (('single_shot', 'dormant'), lambda: self.operatingmode != 4),
        ])

    def is_sample_pressure_high(self):
        return self.sample_pressure > self.sample_pressure_high_limit

    def is_sample_pressure_low(self):
        return self.sample_pressure < self.sample_pressure_low_limit

    def get_id(self):
        return self.unique_id

    def get_pressure(self):
        return self.sample_pressure

    def get_error(self):
        return self.error

    def is_pump_valve_open(self):
        return self.pump_valve_open

    def is_buffer_valve_open(self):
        return self.buffer_valve_open

    def is_gas_valve_open(self):
        return self.gas_valve_open

    def get_operating_mode(self):
        return self.operatingmode

    def is_buffer_pressure_high(self):
        return self.buffer_pressure_high