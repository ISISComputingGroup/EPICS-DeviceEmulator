from collections import OrderedDict

from enum import Enum

from states import StoppedState, MovingState, ErrorState
from lewis.devices import StateMachineDevice

HARD_LIMIT_MINIMUM = 0.0
HARD_LIMIT_MAXIMUM = 5000.0

states = OrderedDict([("Stopped", StoppedState()),
                      ("Moving", MovingState()),
                      ("Error", ErrorState())])


class SimulatedLinmot(StateMachineDevice):

    inside_hard_limits = False

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.position = 0
        self.target_position = 0
        self.inside_hard_limits = True

        self.velocity = 52
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
            (("Stopped", "Moving"), lambda: self.new_action is True and self.position_reached is False),
            (("Moving", "Stopped"), lambda: self.position_reached is True),
            (("Moving", "Error"), lambda: self.inside_hard_limits is False),
            (("Stopped", "Error"), lambda: self.inside_hard_limits is False),
            (("Error", "Stopped"), lambda: self.inside_hard_limits is True)
        ])

    @property
    def state(self):
        return self._csm.state

    def is_within_hard_limits(self):
        """
        Determine if the axis position is within the physics limits of the devices capability.

        The axis has a range of moment, however if taken beyond these then it will put the controller into an
        error state.
        """
        return False if self.position < HARD_LIMIT_MINIMUM or self.position > HARD_LIMIT_MAXIMUM else True

    def move_to_target(self, target_position):
        """
        Demand the motor to drive to a target position.

        Argument(s):
            target_position (int): the desire axis target position
        """
        if self.is_within_hard_limits():
            self.new_action = True
            self.position_reached = False
            self.target_position = target_position
        return

    def _get_state_handlers(self):
        return states

    def _get_initial_state(self):
        return "Stopped"

    def reset(self):
        self._initialize_data()
