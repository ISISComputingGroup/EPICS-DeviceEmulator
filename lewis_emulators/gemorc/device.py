from collections import OrderedDict
from states import StoppedState, OscillatingState, InitialisingState, IdleState, InitialisedState
from lewis.devices import StateMachineDevice

SMALL = 1.0e-10

class SimulatedGemorc(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        # State control variables
        self.time_to_initialise = 2.0
        self.time_spent_initialising = 0.0
        self.initialisation_requested = False
        self.start_requested = False
        self.state = None  # Controlled by state handler
        self.stop_initialisation = False

        self.initialisation_cycle = 20000
        self.optional_initialisation_cycle = 10000
        self.complete_cycles = 0

        # Device settings
        self.window_width = 100
        self.acceleration = 500
        self.target_speed = 20
        self.speed = 0
        self.offset = 0
        self.backlash = 10

    def _get_state_handlers(self):
        return {
            'initialising': InitialisingState(),
            'initialised': InitialisedState(),
            'oscillating': OscillatingState(),
            'stopped': StoppedState(),
            'idle': IdleState(),
        }

    def _get_initial_state(self):
        return 'idle'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('idle', 'initialising'), lambda: self.initialisation_requested),

            (('initialising', 'initialised'), lambda: self.time_spent_initialising >= self.time_to_initialise),

            (('initialised', 'oscillating'), lambda: self.start_requested),
            (('initialised', 'initialising'), lambda: self.initialisation_requested),

            (('oscillating', 'stopped'), lambda: not self.start_requested),
            # (('oscillating', 'initialising'), lambda: self.complete_cycles > 0 and
            #                                           self.complete_cycles % self.initialisation_cycle == 0),
            #
            # (('stopped', 'initialising'), lambda: self.initialisation_requested),
            # (('stopped', 'oscillating'), lambda: self.start_requested),
        ])

    def initialise(self):
        self.initialisation_requested = True

    def re_zero_to_datum(self):
        raise NotImplementedError()

    def start(self):
        self.start_requested = True

    def stop(self):
        self.start_requested = False

    def stop_next_initialisation(self):
        self.stop_initialisation = True

    def get_window_width(self):
        return self.window_width

    def set_window_width(self, width):
        self.window_width = width

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset

    def get_acceleration(self):
        return self.acceleration

    def set_acceleration(self, acceleration):
        self.acceleration = acceleration

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.target_speed = speed

    def is_oscillating(self):
        return self.state == OscillatingState.__name__

    def is_initialising(self):
        return self.state == InitialisingState.__name__

    def has_been_initialised(self):
        return self.state not in (IdleState.__name__, InitialisingState.__name__)

    def get_complete_cycles(self):
        return self.complete_cycles

    def get_backlash(self):
        return self.backlash