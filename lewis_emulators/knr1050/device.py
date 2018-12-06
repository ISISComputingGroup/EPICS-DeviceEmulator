from states import InitializingState, OffState, IdleState, RunState, HoldState, PurgeState, StandbyState
from lewis.devices import StateMachineDevice
from collections import OrderedDict
import time

states = OrderedDict([
    ('SYS_ST_INITIALIZING', InitializingState()),
    ('SYS_ST_OFF', OffState()),
    ('SYS_ST_IDLE', IdleState()),
    ('SYS_ST_RUN', RunState()),
    ('SYS_ST_HOLD', HoldState()),
    ('SYS_ST_PURGE', PurgeState()),
    ('SYS_ST_STANDBY', StandbyState())])


class SimulatedKnr1050(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.pump_on = False
        self.keep_last_values = False
        self.ramp = False
        self.hold = False
        self.standby = False
        self.initializing = False
        self.remote = False

        self.pressure = 0
        self.pressure_limit_low = 0
        self.pressure_limit_high = 0
        self.flow_rate = 0.01
        self.current_flow_rate = 0.0

        self.concentrations = [100, 0, 0, 0]

        self.curr_program_run_time = False

    def reset(self):
        self._initialize_data()

    @property
    def time_stamp(self):
        """
        Returns:
            (int) current time in ms
        """
        return int(round(time.time() * 1000))

    @property
    def state_num(self):
        return states.keys().index(self.state)

    @property
    def state(self):
        return self._csm.state

    def _get_state_handlers(self):
        return states

    def _get_initial_state(self):
        return 'SYS_ST_OFF'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('SYS_ST_INITIALIZING', 'SYS_ST_IDLE'), lambda: self.initializing is False),
            (('SYS_ST_RUN', 'SYS_ST_OFF'), lambda: self.pump_on is False),
            (('SYS_ST_OFF', 'SYS_ST_RUN'), lambda: self.pump_on and self.keep_last_values is True),
            (('SYS_ST_RUN', 'SYS_ST_HOLD'), lambda: self.hold is True),
            (('SYS_ST_RUN', 'SYS_ST_STANDBY'), lambda: self.standby is True)
        ])
