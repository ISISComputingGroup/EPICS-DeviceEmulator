from collections import OrderedDict
from states import StoppedState, OscillatingState, InitialisingState, IdleState, InitialisedState, ResetState
from lewis.devices import StateMachineDevice

SMALL = 1.0e-10

class SimulatedGemorc(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        # State control variables
        self.time_to_initialise = 300.0  # 3s in real time with speed up factor of 100
        self.time_spent_initialising = 0.0
        self.state = None  # Controlled by state handler

        # Device settings, set by the reset state
        self.window_width = 0
        self.acceleration = 0
        self.speed = 0
        self.offset = 0
        self.initialisation_requested = False
        self.start_requested = False
        self.stop_initialisation = False

        # Instantaneous properties
        self.complete_cycles = 0

        # Emulator control
        self.reset = False

    def _get_state_handlers(self):
        return {
            'initialising': InitialisingState(),
            'initialised': InitialisedState(),
            'oscillating': OscillatingState(),
            'stopped': StoppedState(),
            'idle': IdleState(),
            'reset': ResetState(),
        }

    def _get_initial_state(self):
        return 'reset'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('idle', 'initialising'), lambda: self.initialisation_requested),

            (('initialising', 'initialised'), lambda: self.stop_initialisation or
                                                      self.time_spent_initialising >= self.time_to_initialise),

            (('initialised', 'oscillating'), lambda: self.start_requested),
            (('initialised', 'initialising'), lambda: self.initialisation_requested),

            (('oscillating', 'stopped'), lambda: not self.start_requested),
            (('oscillating', 'initialising'), lambda: self.initialisation_requested),

            (('stopped', 'initialising'), lambda: self.initialisation_requested),
            (('stopped', 'oscillating'), lambda: self.start_requested),

            (('idle', 'reset'), lambda: self.reset),
            (('initialising', 'reset'), lambda: self.reset),
            (('initialised', 'reset'), lambda: self.reset),
            (('oscillating', 'reset'), lambda: self.reset),
            (('stopped', 'reset'), lambda: self.reset),
            (('reset', 'idle'), lambda: not self.reset),
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
        self.speed = speed

    def is_oscillating(self):
        return self.state == OscillatingState.__name__

    def is_initialising(self):
        return self.state == InitialisingState.__name__

    def has_been_initialised(self):
        return self.state in (s.__name__ for s in (InitialisedState, OscillatingState, StoppedState))

    def get_complete_cycles(self):
        return self.complete_cycles

    def get_backlash(self):
        return 0.5*float(self.speed**2)/float(max(self.acceleration,1))