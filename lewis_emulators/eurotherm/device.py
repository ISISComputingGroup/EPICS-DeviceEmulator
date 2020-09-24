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
        self.connected = True

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
        """
        Get the address of the device.

        Returns: the address of the device e.g. "A01"
        """
        return self._address

    @address.setter
    def address(self, addr):
        """
        Sets the address of the device.

        Args:
            addr (str): the address of this device e.g. "A01".

        """
        self._address = addr

    @property
    def current_temperature(self):
        """
        Get current temperature of the device.

        Returns: the current temperature in K.
        """
        return self._current_temperature

    @current_temperature.setter
    def current_temperature(self, temp):
        """
        Set the current temperature of the device.

        Args:
            temp: the current temperature of the device in K.

        """
        self._current_temperature = temp

    @property
    def ramping_on(self):
        """
        Gets whether the device is currently ramping.

        Returns: bool indicating if the device is ramping.
        """
        return self._ramping_on

    @ramping_on.setter
    def ramping_on(self, toggle):
        """
        Sets whether the device is currently ramping.

        Args:
            toggle (bool): turn ramping on or off.

        """
        self._ramping_on = toggle

    @property
    def ramp_rate(self):
        """
        Get the current ramp rate.

        Returns: the current ramp rate in K/min
        """
        return self._ramp_rate

    @ramp_rate.setter
    def ramp_rate(self, ramp_rate):
        """
        Set the ramp rate.

        Args:
            ramp_rate (float): set the current ramp rate in K/min.

        """
        self._ramp_rate = ramp_rate

    @property
    def ramp_setpoint_temperature(self):
        """
        Get the set point temperature.

        Returns: the current value of the setpoint temperature in K.
        """
        return self._ramp_setpoint_temperature

    @ramp_setpoint_temperature.setter
    def ramp_setpoint_temperature(self, temp):
        """
        Set the set point temperature.

        Args:
            temp (float): the current value of the set point temperature in K.

        """
        self._ramp_setpoint_temperature = temp

