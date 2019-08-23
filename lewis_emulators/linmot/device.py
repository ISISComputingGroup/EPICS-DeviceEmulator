from collections import OrderedDict
from states import StoppedState, MovingState, ErrorState
from lewis.devices import StateMachineDevice

states = OrderedDict([("Stopped", StoppedState()),
                      ("Moving", MovingState()),
                      ("Error", ErrorState())])


class SimulatedLinmot(StateMachineDevice):

    def __init__(self, override_states=None, override_transitions=None,
                 override_initial_state=None, override_initial_data=None):

        super(SimulatedLinmot, self).__init__(override_states=None, override_transitions=None,
                                              override_initial_state=None, override_initial_data=None)
        self.inside_limits = False

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.position = 0
        self.target_position = 0
        self.minimum_value = 0.0
        self.maximum_value = 10000
        self.inside_limits = True

        self.velocity = 52
        self.maximal_speed = 52
        self.maximal_acceleration = 10
        self.speed_resolution = 190735

        self.motor_warn_status = 256
        self.motor_error_status = 0

        self.new_action = False
        self.position_reached = False
        self.tolerance = 0.01

        self.connected = True

    def _get_transition_handlers(self):
        return OrderedDict([
            (("Stopped", "Moving"), lambda: self.new_action is True),
            (("Moving", "Stopped"), lambda: self.position_reached is True),
            (("Moving", "Error"), lambda: self.inside_limits is False),
            (("Stopped", "Error"), lambda: self.inside_limits is False)
        ])

    @property
    def state(self):
        return self._csm.state

    def is_within_hard_limits(self):
        if self.position > self.maximum_value or self.position < self.minimum_value:
            self.inside_limits = False
        else:
            self.inside_limits = True
        return

    def _get_state_handlers(self):
        return states

    def _get_initial_state(self):
        return "Stopped"

    def reset(self):
        self._initialize_data()
