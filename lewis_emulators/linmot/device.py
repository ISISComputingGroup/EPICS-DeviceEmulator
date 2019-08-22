from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


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

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def reset(self):
        self._initialize_data()
