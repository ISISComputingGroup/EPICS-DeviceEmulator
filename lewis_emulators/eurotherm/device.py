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
        self._flow = 5.0
        self._manual_flow = 6.0
        self._flow_low_lim = 1.0
        self._flow_sp_mode = 1
        self._valve_direction = 1
        self.p = 0
        self.i = 0
        self.d = 0
        self.autotune = 0
        self.max_output = 0
        self.output = 0
        self.high_lim = 0
        self.low_lim = 0
        self.flow_high_lim = 2.0
        

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
    
    @property
    def flow(self):
        """
        Get the flow readback from the transducer

        Returns: the current value of the flow rate in L/min
        """
        return self._flow

    @property
    def manual_flow(self):
        """
        Get the manual flow setpoint

        Returns: the current value of the manual flow setpoint
        """
        return self._manual_flow

    @manual_flow.setter
    def manual_flow(self, flow_val):
        """
        Sets the manual flow setpoint

        Args:
            flow_val (float): set the manual flow setpoint in L/min
        """
        self._manual_flow = flow_val
    
    @property
    def flow_low_lim(self):
        """
        Get the low setpoint limit for flow control

        Returns: the current value of the manual flow setpoint
        """
        return self._flow_low_lim

    @flow_low_lim.setter
    def flow_low_lim(self, low_lim):
        """
        Sets the low setpoint limit for flow control

        Args:
            low_lim (float): set the low setpoint limit in L/min
        """
        self._flow_low_lim = low_lim

    @property
    def flow_sp_mode(self):
        """
        Get the mode of the flow setpoint 

        Returns: current mode of the flow setpoint (AUTO/MANUAL)
        """
        return self._flow_sp_mode

    @flow_sp_mode.setter
    def flow_sp_mode(self, mode):
        """
        Sets the mode of the flow setpoint 

        Args:
            mode (int)
        """
        self._flow_sp_mode = mode

    @property
    def valve_direction(self):
        """
        Get the direction of the valve 

        Returns: current direction of the valve (OPENING/CLOSING)
        """
        return self._valve_direction
