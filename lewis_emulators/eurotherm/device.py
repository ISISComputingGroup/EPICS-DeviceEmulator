from collections import OrderedDict
from time import sleep

from lewis.devices import StateMachineDevice
from .states import DefaultState
from lewis.core.logging import has_log

@has_log
class SimulatedEurotherm(StateMachineDevice):
    """
    Simulated Eurotherm device.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self._connected = True
        self.delay_time = None
        self.sensors = {
            "01" : SimulatedEurotherm.EurothermSensor(), 
            "02" : SimulatedEurotherm.EurothermSensor(), 
            "03" : SimulatedEurotherm.EurothermSensor(),
            "04": SimulatedEurotherm.EurothermSensor(),
            "05": SimulatedEurotherm.EurothermSensor(),
            "06": SimulatedEurotherm.EurothermSensor()
        }

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

    def setpoint_temperature(self, addr):
        """
        Get current temperature of the device.

        Returns: the current temperature in K.
        """
        self._delay()
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError            
        return euro.setpoint_temperature

    def set_setpoint_temperature(self, addr, value):
        """
        Set the current temperature of the device.

        Args:
            temp: the current temperature of the device in K.

        """
        value = float(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.current_temperature = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError 
            euro.setpoint_temperature = value
    
    def current_temperature(self, addr):
        """
        Get current temperature of the device.

        Returns: the current temperature in K.
        """
        self._delay()
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError            
        return euro.current_temperature
        

    def set_current_temperature(self, addr, value):
        """
        Set the current temperature of the device.

        Args:
            temp: the current temperature of the device in K.

        """
        value = float(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.current_temperature = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError  
            euro.current_temperature = value

    def address(self, addr):
        """
        Get the address of the device.

        Returns: the address of the device e.g. "A01"
        """
        self._delay()
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError             
        return euro.address

    def set_address(self, addr):
        """
        Sets the address of the device.

        Args:
            addr (str): the address of this device e.g. "A01".

        """
        
        if addr is None:
            euro.address = "01"
        else:
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
        return euro.ramping_on
    
    def set_ramping_on(self, addr, value):
        """
        Sets whether the device is currently ramping.

        Args:
            value - toggle (bool): turn ramping on or off.

        """
        value = bool(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.ramping_on = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.ramping_on = value

    def ramp_rate(self, addr):
        """
        Get the current ramp rate.

        Returns: the current ramp rate in K/min
        """
        self._delay()
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError #not sure if this is right
        return euro.ramp_rate

    
    def set_ramp_rate(self, addr, value):
        """
        Set the ramp rate.

        Args:
            value - ramp_rate (float): set the current ramp rate in K/min.

        """
        value = float(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.ramp_rate = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.ramp_rate = value

    def ramp_setpoint_temperature(self, addr):
        """
        Get the set point temperature.

        Returns: the current value of the setpoint temperature in K.
        """
        self._delay()
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro.ramp_setpoint_temperature

    def set_ramp_setpoint_temperature(self, addr, value):
        """
        Set the set point temperature.

        Args:
            value - temp (float): the current value of the set point temperature in K.

        """
        value = float(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.ramp_setpoint_temperature = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.ramp_setpoint_temperature = value

    def needlevalve_flow(self, addr):
        """
        Get the flow readback from the transducer

        Returns: the current value of the flow rate in L/min
        """
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro.needlevalve_flow
    
    def set_needlevalve_flow(self, addr, value):
        """
        Sets the flow readback from the transducer

        Args: 
            value - flow (double) the current value of the flow rate in L/min
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.needlevalve_flow = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.needlevalve_flow = value

    def needlevalve_manual_flow(self, addr):
        """
        Get the manual flow setpoint

        Returns: the current value of the manual flow setpoint
        """
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro.needlevalve_manual_flow

    def set_needlevalve_manual_flow(self, addr, value):
        """
        Sets the manual flow setpoint

        Args:
            value - flow_val (float): set the manual flow setpoint in L/min
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.needlevalve_manual_flow = value
        else:
            
            
            euro = self.sensors[addr]
            if not euro. connected:
                raise ValueError
            euro.needlevalve_manual_flow = value

    def needlevalve_flow_low_lim(self, addr):
        """
        Get the low setpoint limit for flow control

        Returns: the current value of the manual flow setpoint
        """
        
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro.needlevalve_flow_low_lim

    def set_needlevalve_flow_low_lim(self, addr, value):
        """
        Sets the low setpoint limit for flow control

        Args:
            value - low_lim (float): set the low setpoint limit in L/min
        """
        value = float(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.needlevalve_flow_low_lim = value
        else:
            
            euro = self.sensors[addr]
            if not euro. connected:
                raise ValueError
            euro.needlevalve_flow_low_lim = value

    def needlevalve_flow_high_lim(self, addr):
        """
        Get the low setpoint limit for flow control

        Returns: the current value of the manual flow setpoint
        """
        
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro.needlevalve_flow_high_lim

    
    def set_needlevalve_flow_high_lim(self, addr, value):
        """
        Sets the high setpoint limit for flow control

        Args:
            value - high_lim (float): set the high setpoint limit in L/min
        """
        value = float(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.needlevalve_flow_high_lim = value
        else:
            
            euro = self.sensors[addr]
            if not euro. connected:
                raise ValueError
            euro.needlevalve_flow_high_lim = value

    
    def needlevalve_auto_flow_scale(self, addr):
        """
        Get the auto_flow_scale

        Returns: the current value of the manual flow setpoint
        """
        
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro._needlevalve_auto_flow_scale

    
    def set_needlevalve_auto_flow_scale(self, addr, value):
        """
        Sets the auto_flow_scale

        Args:
            value (float): set the high setpoint limit in L/min
        """
        value = float(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.needlevalve_auto_flow_scale = value
        else:
            
            euro = self.sensors[addr]
            if not euro. connected:
                raise ValueError
            euro.needlevalve_auto_flow_scale = value

    
    def needlevalve_min_auto_flow_bl_temp(self, addr):
        """
        Get min_auto_flow_bl_tempw setpoint

        Returns: current mode of the fmin_auto_flow_bl_temp
        """
        
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro.needlevalve_min_auto_flow_bl_temp

    def set_needlevalve_min_auto_flow_bl_temp(self, addr, value):
        """
        Sets the  min_auto_flow_bl_temp setpoint

        Args:
            value (int)
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.needlevalve_min_auto_flow_bl_temp = value
        else:
            
            euro = self.sensors[addr]
            if not euro. connected:
                raise ValueError
            euro.needlevalve_min_auto_flow_bl_temp = value

    def needlevalve_flow_sp_mode(self, addr):
        """
        Get the mode of the flow setpoint 

        Returns: current mode of the flow setpoint (AUTO/MANUAL)
        """
        
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro.needlevalve_flow_sp_mode

    def set_needlevalve_flow_sp_mode(self, addr, value):
        """
        Sets the mode of the flow setpoint 

        Args:
            value - mode (int)
        """
        value = int(value) 
        if addr is None:
            for euro in self.sensors.values():
                euro.needlevalve_flow_sp_mode = value
        else:
            
            euro = self.sensors[addr]
            if not euro. connected:
                raise ValueError
            euro.needlevalve_flow_sp_mode = value

    def needlevalve_direction(self, addr):
        """
        Get the direction of the valve 

        Returns: current direction of the valve (OPENING/CLOSING)
        """
        
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro.needlevalve_direction
    
    def set_needlevalve_direction(self, addr, value):
        """
        Sets the direction of the valve 

        Args: 
            value - dir (int) current direction of the valve (OPENING/CLOSING)
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.needlevalve_direction = value
        else:
            
            euro = self.sensors[addr]
            if not euro. connected:
                raise ValueError
            euro.needlevalve_direction = value
    
    def needlevalve_stop(self, addr):
        """
        Gets the control mode of Loop 2 

        Returns: current control mode of Loop 2 (STOPPED/NOT STOPPED)
        """
        
        euro = self.sensors[addr]
        if not euro. connected:
            raise ValueError
        return euro.needlevalve_stop
    
    def set_needlevalve_stop(self, addr, value):
        """
        Sets the control mode of Loop 2 

        Args:
            value - stop_val (int)
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.needlevalve_stop = value
        else:
            
            euro = self.sensors[addr]
            if not euro. connected:
                raise ValueError
            euro.needlevalve_stop = value

    def high_lim(self, addr):
        """
        Gets the high limit
        """
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro.high_lim

    def set_high_lim(self, addr, value):
        """
        Sets the high limit
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.high_lim = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.high_lim = value

    def low_lim(self, addr):
        """
        Gets the low limit
        """
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro.low_lim

    def set_low_lim(self, addr, value):
        """
        Sets the low limit
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.low_lim = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.low_lim = value

    def output(self, addr):
        """
        Gets the output value
        """
        
        euro = self.sensors[addr]
        if not euro.connected: 
            raise ValueError
        return euro.output
    
    def set_output(self, addr, value):
        """
        Sets the output value
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.output = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.output = value

    def max_output(self, addr):
        """
        Gets the max output value
        """
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro.max_output
    
    def set_max_output(self, addr, value):
        """
        Sets the max_output value
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.max_output = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
        euro.max_output = value

    def output_rate(self, addr):
        """
        Get the set point output rate.
        """
        self._delay()
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro.output_rate
            
    def set_output_rate(self, addr, value):
        """
        Set the set point output rate.
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.output_rate = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.output_rate = value

    def error(self, addr):
        """
        Gets the error status
        """
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro.error
    
    def set_error(self, addr, error):
        """
        Sets the error status
        """
        error = int(error)
        if addr is None:
            for euro in self.sensors.values():
                euro.error = error
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.error = error

    def scaling(self, addr):
        """
        Gets the scaling factor
        """
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro.scaling
    
    def set_scaling(self, addr, value):
        """
        Sets the scaling factor
        """
        value = float(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.scaling = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.scaling = value

    def autotune(self, addr):
        """
        Gets the autotune value
        """
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro.autotune
    
    def set_autotune(self, addr, value):
        """
        Sets the autotune value
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.autotune = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.autotune = value

    def p(self, addr):
        """
        Gets the autotune value
        """
        print(addr)
        
        euro = self.sensors[addr]
        print(euro)
        if not euro.connected:
            raise ValueError
        return euro.p
    
    def set_p(self, addr, value):
        """
        Sets the autotune value
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.p = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.p = value

    def i(self, addr):
        """
        Gets the autotune value
        """
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro.i
    
    def set_i(self, addr, value):
        """
        Sets the autotune value
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.i = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.i = value

    def d(self, addr):
        """
        Gets the autotune value
        """
        
        euro = self.sensors[addr]
        if not euro.connected:
            raise ValueError
        return euro.d
    
    def set_d(self, addr, value):
        """
        Sets the autotune value
        """
        value = int(value)
        if addr is None:
            for euro in self.sensors.values():
                euro.d = value
        else:
            
            euro = self.sensors[addr]
            if not euro.connected:
                raise ValueError
            euro.d = value
    
    def connected(self, addr):
        """
        Gets connected status
        """
        euro = self.sensors[addr]
        return euro.connected

    def set_connected(self, addr, connected):
        """
        Sets connected status
        """
        self.log.info(f"Addr: {addr}, Connected: {connected}")
        self.log.info(f"{addr.__class__.__name__}")
        connected = bool(connected)
        if addr is None:
            for euro in self.sensors.values():
                euro.connected = connected
        else:
            euro = self.sensors[addr]
            euro.connected = connected

    class EurothermSensor():
        """
        Eurotherm temperature sensor method
        """

        def __init__(self):
            self.connected = True
            self.current_temperature = 0.0
            self.setpoint_temperature = 0.0
            self.address = None
            self.p = 0
            self.i = 0
            self.d = 0
            self.autotune = 0
            self.output = 0
            self.output_rate = 0
            self.max_output = 0
            self.high_lim = 0
            self.low_lim = 0
            self.error = "0"
            self.scaling = 1.0
            self.ramping_on = False
            self.ramp_rate = 1.0
            self.ramp_setpoint_temperature = 0.0
            self.needlevalve_flow = 0
            self.needlevalve_manual_flow = 0
            self.needlevalve_flow_low_lim = 0
            self.needlevalve_flow_high_lim = 0
            self.needlevalve_auto_flow_scale = 0
            self.needlevalve_min_auto_flow_bl_temp = 0
            self.needlevalve_flow_sp_mode = 0
            self.needlevalve_direction = ""
            self.needlevalve_stop = 0
        