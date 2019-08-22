from collections import OrderedDict
from states import StoppedState, MovingState
from lewis.devices import StateMachineDevice

states = OrderedDict([("Stopped", StoppedState()),
                      ("Moving", MovingState())])


class SimulatedLinmot(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.position = 0
        self.velocity = 1
        self.motor_warn_status = 256
        self.motor_error_status = 0
        self.maximal_speed = 52
        self.maximal_acceleration = 10
        self.target_position = 0
        self.new_action = False
        self.position_reached = False
        self.tolerance = 0.01

    def _get_transition_handlers(self):
        return OrderedDict([
            (('Stopped', 'Moving'), lambda: self.new_action is True),
            (("Moving", "Stopped"), lambda: self.position_reached is True)
        ])

    @property
    def state(self):
        return self._csm.state

    def _get_state_handlers(self):
        return states

    def _get_initial_state(self):
        return "Stopped"

    def reset(self):
        self._initialize_data()
