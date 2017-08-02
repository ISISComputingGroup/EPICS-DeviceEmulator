from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class SimulatedCybaman(StateMachineDevice):
    """
    Simulated cyber man.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self.a = 0
        self.b = 0
        self.c = 0

        self.home_position_axis_a = 66
        self.home_position_axis_b = 77
        self.home_position_axis_c = 88

    def _get_state_handlers(self):
        """
        Returns: states and their names
        """
        return {DefaultState.NAME: DefaultState()}

    def _get_initial_state(self):
        """
        Returns: the name of the initial state
        """
        return DefaultState.NAME

    def _get_transition_handlers(self):
        """
        Returns: the state transitions
        """
        return OrderedDict()

    def home_axis_a(self):
        self.a = self.home_position_axis_a

    def home_axis_b(self):
        self.b = self.home_position_axis_b

    def home_axis_c(self):
        self.c = self.home_position_axis_c



