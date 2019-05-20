from collections import OrderedDict
from states import InfusingState, WithdrawingState, PumpingProgramStoppedState, PumpingProgramPausedState, PausePhaseState, UserWaitState
from lewis.devices import StateMachineDevice

states = OrderedDict([
    ('I', InfusingState()),
    ('W', WithdrawingState()),
    ('S', PumpingProgramStoppedState()),
    ('P', PumpingProgramPausedState()),
    ('T', PausePhaseState()),
    ('U', UserWaitState())])


class SimulatedAldn1000(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.input_correct = True

        self._pump_on = False
        self.program_function = 'RAT'

        self.address = 0
        self._diameter = 0.0
        self.volume = 0.0
        self.volume_infused = 0.0  # Cumulative infused volume
        self.volume_withdrawn = 0.0  # Cumulative withdrawn volume
        self.volume_dispensed = 0.0  # Dispensed volume for a single pump run
        self._direction = 'INF'
        self.rate = 0.0
        self.units = 'UM'
        self.volume_units = 'UL'
        self.new_action = False

    def clear_volume(self, volume_type):
        if volume_type == 'INF':
            self.volume_infused = 0.0
        elif volume_type == 'WDR':
            self.volume_withdrawn = 0.0
        return

    @property
    def pump_on(self):
        return self._pump_on

    @pump_on.setter
    def pump_on(self, action):
        self.new_action = True  # Check used for On -> Paused / Paused -> Off state transition.
        if action == 'STP':
            self._pump_on = False
        elif action == 'RUN':
            self._pump_on = True
        else:
            print('An error occurred while trying to start/stop the pump')

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, new_value):
        if new_value > 14.0:  # Device changes the volume units automatically based on the diameter set
            self.volume_units = 'ML'
        else:
            self.volume_units = 'UL'
        self._diameter = new_value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_direction):
        if new_direction == 'REV':  # Reverse
            if self._direction == 'INF':  # Infuse
                self._direction = 'WDR'  # Withdraw
            else:
                self._direction = 'INF'
        else:
            self._direction = new_direction

    def reset(self):
        self._initialize_data()

    @property
    def state(self):
        return self._csm.state

    def _get_state_handlers(self):
        return states

    def _get_initial_state(self):
        return 'S'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('S', 'I'), lambda: self.pump_on is True and self.direction == 'INF'),
            (('S', 'W'), lambda: self.pump_on is True and self.direction == 'WDR'),
            (('I', 'P'), lambda: self.pump_on is False),
            (('W', 'P'), lambda: self.pump_on is False),
            (('P', 'S'), lambda: self.pump_on is False and self.new_action is True),
            (('P', 'I'), lambda: self.pump_on is True and self.direction == 'INF'),
            (('P', 'W'), lambda: self.pump_on is True and self.direction == 'WDR'),
        ])

