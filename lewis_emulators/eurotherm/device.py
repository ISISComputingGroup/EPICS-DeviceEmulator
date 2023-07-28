from collections import OrderedDict
from time import sleep

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
        self.delay_time = None

        self._current_temperature = 0.0
        self._setpoint_temperature = 0.0
        self._ramp_setpoint_temperature = 0.0
        self._ramping_on = False
        self._ramp_rate = 1.0
        self._address = "A1"
        self._needlevalve_flow = 0
        self._needlevalve_manual_flow = 0
        self._needlevalve_flow_low_lim = 0
        self._needlevalve_flow_sp_mode = 0
        self._needlevalve_direction = 0
        self._needlevalve_stop = 0
        self.p = 0
        self.i = 0
        self.d = 0
        self.autotune = 0
        self.max_output = 0
        self._output_rate = 0
        self.output = 0
        self.high_lim = 0
        self.low_lim = 0
        self.error = "0"

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
    
    def _delay(self):
        """
        Simulate a delay.
        """
        if self.delay_time is not None:
            sleep(self.delay_time)

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
        self._delay()
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
        self._delay()
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
        self._delay()
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
        self._delay()
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
    def output_rate(self):
        """
        Get the set point output rate.
        """
        self._delay()
        return self._output_rate
        
    @output_rate.setter
    def output_rate(self, value):
        """
        Set the set point output rate.
        """
        self._output_rate = value

    @property
    def needlevalve_flow(self):
        """
        Get the flow readback from the transducer

        Returns: the current value of the flow rate in L/min
        """
        return self._needlevalve_flow
    
    @needlevalve_flow.setter
    def needlevalve_flow(self, flow):
        """
        Sets the flow readback from the transducer

        Args: 
            flow (double) the current value of the flow rate in L/min
        """
        self._needlevalve_flow = flow

    @property
    def needlevalve_manual_flow(self):
        """
        Get the manual flow setpoint

        Returns: the current value of the manual flow setpoint
        """
        return self._needlevalve_manual_flow

    @needlevalve_manual_flow.setter
    def needlevalve_manual_flow(self, flow_val):
        """
        Sets the manual flow setpoint

        Args:
            flow_val (float): set the manual flow setpoint in L/min
        """
        self._needlevalve_manual_flow = flow_val
    
    @property
    def needlevalve_flow_low_lim(self):
        """
        Get the low setpoint limit for flow control

        Returns: the current value of the manual flow setpoint
        """
        return self._needlevalve_flow_low_lim

    @needlevalve_flow_low_lim.setter
    def needlevalve_flow_low_lim(self, low_lim):
        """
        Sets the low setpoint limit for flow control

        Args:
            low_lim (float): set the low setpoint limit in L/min
        """
        self._needlevalve_flow_low_lim = low_lim

    @property
    def needlevalve_flow_sp_mode(self):
        """
        Get the mode of the flow setpoint 

        Returns: current mode of the flow setpoint (AUTO/MANUAL)
        """
        return self._needlevalve_flow_sp_mode

    @needlevalve_flow_sp_mode.setter
    def needlevalve_flow_sp_mode(self, mode):
        """
        Sets the mode of the flow setpoint 

        Args:
            mode (int)
        """
        self._needlevalve_flow_sp_mode = mode

    @property
    def needlevalve_direction(self):
        """
        Get the direction of the valve 

        Returns: current direction of the valve (OPENING/CLOSING)
        """
        return self._needlevalve_direction
    
    @needlevalve_direction.setter
    def needlevalve_direction(self, dir):
        """
        Sets the direction of the valve 

        Args: 
            dir (int) current direction of the valve (OPENING/CLOSING)
        """
        self._needlevalve_direction = dir
    
    @property
    def needlevalve_stop(self):
        """
        Gets the control mode of Loop 2 

        Returns: current control mode of Loop 2 (STOPPED/NOT STOPPED)
        """
        return self._needlevalve_stop
    
    @needlevalve_stop.setter
    def needlevalve_stop(self, stop_val):
        """
        Sets the control mode of Loop 2 

        Args:
            stop_val (int)
        """
        self._needlevalve_stop = stop_val

