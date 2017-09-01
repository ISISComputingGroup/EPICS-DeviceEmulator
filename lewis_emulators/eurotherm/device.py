from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class SimulatedEurotherm(StateMachineDevice):
    """
    Simulated Eurotherm temperature sensor.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self._current_temperature = 0.0
        self._setpoint_temperature = 0.0
        self._ramp_setpoint_temperature = 0.0
        self._ramping_on = False
        self._ramp_rate = 1.0
        self._address = "A1"

    def _get_state_handlers(self):
        """
        Returns: states and their names
        """
        return {
            DefaultState.NAME: DefaultState()
        }

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

    @property
    def address(self):
        self._address

    @address.setter
    def address(self, addr):
        self._address = addr

    @property
    def current_temperature(self):
        return self._current_temperature

    @current_temperature.setter
    def current_temperature(self, temp):
        self._current_temperature = temp

    @property
    def ramping_on(self):
        return self._ramping_on

    @ramping_on.setter
    def ramping_on(self, toggle):
        self._ramping_on = toggle

    @property
    def ramp_rate(self):
        return self._ramp_rate

    @ramp_rate.setter
    def ramp_rate(self, ramp_rate):
        self._ramp_rate = ramp_rate

    @property
    def ramp_setpoint_temperature(self):
        return self._ramp_setpoint_temperature

    @ramp_setpoint_temperature.setter
    def ramp_setpoint_temperature(self, temp):
        self._ramp_setpoint_temperature = temp

