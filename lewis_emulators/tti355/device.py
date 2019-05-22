from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from random import random


class SimulatedTti355(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.ident = "THURLBY EX355P, <version>"
        self.voltage = 1.00
        self.voltage_sp = 1.00
        self.current = 1.00
        self.current_sp = 1.00
        self.output_status = "OUT OFF"
        self.output_status_sp = "OUT OFF"
        self.output_mode = "M CC"
        self.output_mode_sp = "M CC"
        self.error = 0

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
        return self.voltage()
    
    def set_voltage_sp(self, voltage):
        voltage = round(float(voltage), 2)
        if voltage > self._max_voltage:
            self.error = 2
        else:
            self.voltage_sp = voltage

    
    def get_current(self):
        pass
    
    def set_current_sp(self):
        pass
    
    def set_output_status(self):
        pass

    def get_output_status(self):
        pass

    def set_output_mode(self):
        pass

    def get_output_mode(self):
        pass        
    
    def get_ident(self):
        pass
    
    def get_error(self):
        pass