from lewis.devices import StateMachineDevice
from states import DefaultState, MovingState
from collections import OrderedDict


class SimulatedAttocubeANC350(StateMachineDevice):
    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.position = 0
        self.position_setpoint = 0
        self.speed = 10
        self.start_move = False

    def move(self):
        self.start_move = True

    def set_position_setpoint(self, position):
        self.position_setpoint = position

    def _get_state_handlers(self):
        return {DefaultState.NAME: DefaultState(),
                MovingState.NAME: MovingState()}

    def _get_initial_state(self):
        return DefaultState.NAME

    def _get_transition_handlers(self):
        return OrderedDict([
            ((DefaultState.NAME, MovingState.NAME), lambda: self.start_move),
            ((MovingState.NAME, DefaultState.NAME), lambda: self.position_setpoint == self.position),
        ])
