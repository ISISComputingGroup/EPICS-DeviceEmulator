from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class SimulatedFZJDDFCH(StateMachineDevice):
    """
    Simulated FZJ Digital Drive Fermi Chopper Controller.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self.frequency_reference = 0
        self.frequency_setpoint = 0
        self.frequency = 0
        self.phase_setpoint = 0
        self.phase = 0
        self.phase_status = "NOK"
        self.magnetic_bearing = "OFF"
        self.magnetic_bearing_status = "NOK"

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
