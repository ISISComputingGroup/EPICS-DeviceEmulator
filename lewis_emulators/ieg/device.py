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

        self.error = 0

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

