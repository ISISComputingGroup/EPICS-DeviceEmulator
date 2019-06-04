from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from random import random


class SimulatedTti355(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.identity = "Thurlby Thandar,EL302P,0,v1.14"
        self.voltage = 0.00
        self.voltage_sp = 1.00
        self.current = 0.00
        self.current_limit_sp = 1.00
        self.output_status = "OUT Off"
        self.output_mode = "M CV"
        self.error = "ERR 0"
        self._max_voltage = 35.0
        self._max_current = 5.0
        self.load_resistance = 0.01

    def reset(self):
        self._initialize_data()

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def calculate_load_resistance(self, voltage, current):
        return voltage/current

    def calculate_potential_current(self, voltage):
        return voltage/self.load_resistance

    def get_voltage(self):
        if self.output_status == "OUT On":
            self.voltage = self.voltage_sp + ((random()-0.5)/1000)
        else:
            self.voltage = ((random()-0.5)/1000)
        return self.voltage
    
    def set_voltage_sp(self, voltage):
        voltage = round(float(voltage), 2)
        if voltage > self._max_voltage:
            self.error = "ERR 2"
        else:
            if self.calculate_potential_current(voltage) > self.get_current():
                self.output_mode = "M CC"
            self.voltage_sp = voltage

    def get_current(self):
        if self.output_status == "OUT On":
            self.current = self.current_limit_sp + ((random()-0.5)/1000)
        else:
            self.current = ((random()-0.5)/1000)
        return self.current
    
    def set_current_limit_sp(self, current):
        current = round(float(current), 2)
        if current > self._max_current:
            self.error = "ERR 2"
        else:
            self.current_limit_sp = current
    
    def set_output_status(self, status):
        if status == "On":
            self.output_status = "OUT On"
        elif status == "Off":
            self.output_status = "OUT Off"
            self.reset()

    def get_output_status(self):
        return self.output_status

    def get_output_mode(self):
        return self.output_mode
    
    def get_error_status(self):
        if self.error == "ERR 1":
            self.error = "ERR 0"
            return "ERR 1"
        elif self.error == "ERR 2":
            self.error = "ERR 0"
            return "ERR 2"
        else:
            return self.error
