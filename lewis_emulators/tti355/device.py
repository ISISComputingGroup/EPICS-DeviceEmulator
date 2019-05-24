from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from random import random


class SimulatedTti355(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.identity = "THURLBY EX355P, <version>"
        self.voltage = 1.00
        self.voltage_sp = 1.00
        self.current = 1.00
        self.current_sp = 1.00
        self.output_status = "OUT OFF"
        self.output_mode = "M CV"
        self.error = 0# "ERR {}".format(0)
        self._max_voltage = 35.0
        self._max_current = 5.0

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

    def get_voltage(self):
        if self.output_status == "OUT ON":
            self.voltage = self.voltage_sp + random()
        else:
            self.voltage = random()
        return self.voltage
    
    def set_voltage_sp(self, voltage):
        voltage = round(float(voltage), 2)
        if voltage > self._max_voltage:
            self.error = 2# "ERR {}".format(2)
        else:
            self.voltage_sp = voltage

    def get_current(self):
        if self.output_status == "OUT ON":
            self.current = self.current_sp + random()
        else:
            self.current = random()
        return self.current
    
    def set_current_sp(self, current):
        current = round(float(current), 2)
        print(self.current_sp)
        if current > self._max_current:
            self.error = 2# "ERR {}".format(2)
            print(self.current_sp)
        else:
            self.current_sp = current
    
    def set_output_status(self, status):
        if status == "ON":
            self.output_status = "OUT ON"
        elif status == "OFF":
            self.output_status = "OUT OFF"
        
    def get_output_status(self):
        return self.output_status

    def get_output_mode(self):
        return self.output_mode
    
    def get_error_status(self):
        return self.error