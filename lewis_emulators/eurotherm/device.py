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
        
        self.sensors = {"0011": self.EurothermSensor(), "0022": self.EurothermSensor(), "0033": self.EurothermSensor()}
        for sensor in self.sensors:
            sensor._initialize_data()

    def _get_state_handlers(self, addr):
        """
        Returns: states and their names
        """
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return {
            DefaultState.NAME: DefaultState()
        }
    
    def _get_initial_state(self, addr):
        """
        Returns: the name of the initial state
        """
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
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

    def current_temperature(self, addr):
        """
        Get current temperature of the device.

        Returns: the current temperature in K.
        """
        self._delay()
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError #not sure if this is right            
        return euro.current_temperature
        

    def set_current_temperature(self, addr, temp):
        """
        Set the current temperature of the device.

        Args:
            temp: the current temperature of the device in K.

        """
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError #not sure if this is right 
        euro.current_temperature = temp

    def address(self, addr):
        """
        Get the address of the device.

        Returns: the address of the device e.g. "A01"
        """
        self._delay()
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError #not sure if this is right            
        return euro.address

    def set_address(self, addr):
        """
        Sets the address of the device.

        Args:
            addr (str): the address of this device e.g. "A01".

        """
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        euro.address = addr

    def ramping_on(self, addr):
        """
        Gets whether the device is currently ramping.

        Returns: bool indicating if the device is ramping.
        """
        self._delay()
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError            
        return euro._ramping_on
    
    def set_ramping_on(self, addr, toggle):
        """
        Sets whether the device is currently ramping.

        Args:
            toggle (bool): turn ramping on or off.

        """
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        euro._ramping_on = toggle

    def ramp_rate(self, addr):
        """
        Get the current ramp rate.

        Returns: the current ramp rate in K/min
        """
        self._delay()
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError #not sure if this is right
        return euro._ramp_rate

    
    def set_ramp_rate(self, addr, ramp_rate):
        """
        Set the ramp rate.

        Args:
            ramp_rate (float): set the current ramp rate in K/min.

        """
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        euro._ramp_rate = ramp_rate

    def ramp_setpoint_temperature(self, addr):
        """
        Get the set point temperature.

        Returns: the current value of the setpoint temperature in K.
        """
        self._delay()
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro._ramp_setpoint_temperature

    def set_ramp_setpoint_temperature(self, addr, temp):
        """
        Set the set point temperature.

        Args:
            temp (float): the current value of the set point temperature in K.

        """
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        euro._ramp_setpoint_temperature = temp

   
    def output_rate(self, addr):
        """
        Get the set point output rate.
        """
        self._delay()
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro._output_rate
        
    def set_output_rate(self, addr, value):
        """
        Set the set point output rate.
        """
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        euro._output_rate = value


    def needlevalve_flow(self, addr):
        """
        Get the flow readback from the transducer

        Returns: the current value of the flow rate in L/min
        """
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro._needlevalve_flow
    
    def set_needlevalve_flow(self, addr, flow):
        """
        Sets the flow readback from the transducer

        Args: 
            flow (double) the current value of the flow rate in L/min
        """
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        euro._needlevalve_flow = flow

    def needlevalve_manual_flow(self, addr):
        """
        Get the manual flow setpoint

        Returns: the current value of the manual flow setpoint
        """
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro._needlevalve_manual_flow

    def set_needlevalve_manual_flow(self, addr, flow_val):
        """
        Sets the manual flow setpoint

        Args:
            flow_val (float): set the manual flow setpoint in L/min
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        euro._needlevalve_manual_flow = flow_val

    def needlevalve_flow_low_lim(self, addr):
        """
        Get the low setpoint limit for flow control

        Returns: the current value of the manual flow setpoint
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro._needlevalve_flow_low_lim

    def set_needlevalve_flow_low_lim(self, addr, low_lim):
        """
        Sets the low setpoint limit for flow control

        Args:
            low_lim (float): set the low setpoint limit in L/min
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        euro._needlevalve_flow_low_lim = low_lim

    def needlevalve_flow_high_lim(self, addr):
        """
        Get the low setpoint limit for flow control

        Returns: the current value of the manual flow setpoint
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro._needlevalve_flow_high_lim

    
    def set_needlevalve_flow_high_lim(self, addr, high_lim):
        """
        Sets the high setpoint limit for flow control

        Args:
            high_lim (float): set the high setpoint limit in L/min
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        euro._needlevalve_flow_high_lim = high_lim

    
    def needlevalve_auto_flow_scale(self, addr):
        """
        Get the auto_flow_scale

        Returns: the current value of the manual flow setpoint
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro._needlevalve_auto_flow_scale

    
    def needlevalve_auto_flow_scale(self, addr, value):
        """
        Sets the auto_flow_scale

        Args:
            value (float): set the high setpoint limit in L/min
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        euro._needlevalve_auto_flow_scale = value

    
    def needlevalve_min_auto_flow_bl_temp(self, addr):
        """
        Get min_auto_flow_bl_tempw setpoint

        Returns: current mode of the fmin_auto_flow_bl_temp
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro._needlevalve_min_auto_flow_bl_temp

    def set_needlevalve_min_auto_flow_bl_temp(self, addr, value):
        """
        Sets the  min_auto_flow_bl_temp setpoint

        Args:
            value (int)
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        euro._needlevalve_min_auto_flow_bl_temp = value

    def needlevalve_flow_sp_mode(self, addr):
        """
        Get the mode of the flow setpoint 

        Returns: current mode of the flow setpoint (AUTO/MANUAL)
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro._needlevalve_flow_sp_mode

    def set_needlevalve_flow_sp_mode(self, addr, mode):
        """
        Sets the mode of the flow setpoint 

        Args:
            mode (int)
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        euro._needlevalve_flow_sp_mode = mode

    def needlevalve_direction(self, addr):
        """
        Get the direction of the valve 

        Returns: current direction of the valve (OPENING/CLOSING)
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro._needlevalve_direction
    
    def set_needlevalve_direction(self, addr, dir):
        """
        Sets the direction of the valve 

        Args: 
            dir (int) current direction of the valve (OPENING/CLOSING)
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        euro._needlevalve_direction = dir
    
    def needlevalve_stop(self, addr):
        """
        Gets the control mode of Loop 2 

        Returns: current control mode of Loop 2 (STOPPED/NOT STOPPED)
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro._needlevalve_stop
    
    def set_needlevalve_stop(self, addr, stop_val):
        """
        Sets the control mode of Loop 2 

        Args:
            stop_val (int)
        """
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        euro._needlevalve_stop = stop_val

    class EurothermSensor():
        """
        Eurotherm Sensor method
        """

        def initialize_data(self):
            self.connected = True
            self.delay_time = None
            self._current_temperature = 0.0
            self._setpoint_temperature = 0.0
            self._ramp_setpoint_temperature = 0.0
            self._ramping_on = False
            self._ramp_rate = 1.0
            self._address = None
            self._needlevalve_flow = 0
            self._needlevalve_manual_flow = 0
            self._needlevalve_flow_low_lim = 0
            self._needlevalve_flow_high_lim = 0
            self._needlevalve_min_auto_flow_bl_temp = 0
            self._needlevalve_auto_flow_scale = 0
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
            self.scaling = 1.0
            self.ramping_on = None
            self.ramp_rate = 0
            self.ramp_setpoint_temperature = 0
            self.output_rate = 0
            self.needlevalve_flow = 0
            self.needlevalve_manual_flow = 0
            self.needlevalve_flow_low_lim = 0
            self.needlevalve_flow_high_lim = 0
            self.needlevalve_auto_flow_scale = 0
            self.needlevalve_min_auto_flow_bl_temp = 0
            self.needlevalve_flow_sp_mode = 0
            self.needlevalve_direction = ""
            self.needlevalve_stop = 0
        