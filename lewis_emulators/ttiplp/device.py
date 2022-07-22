from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice
from random import random as rnd


class SimulatedTtiplp(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.ident = "THURLBY THANDAR, PL303-P, 490296, 3.02-4.06"
        self.volt = 0
        self.volt_sp = 0
        self.curr = 0
        self.curr_sp = 0
        self.output = 0
        self.overvolt = 0
        self.overcurr = 0
        self.ocp_tripped = False
        self.ovp_tripped = False

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

    def get_volt(self):
        if self.output == 1:
            self.volt = self.volt_sp + ((rnd()-0.5)/1000)
        else:
            self.volt = ((rnd()-0.5)/1000)
        return self.volt    

    def get_curr(self):
        if self.output == 1:
            self.curr = self.curr_sp+((rnd()-0.5)/1000)
        else:
            self.curr = ((rnd()-0.5)/1000)
        return self.curr    

    def set_volt_sp(self, volt_sp):
        self.volt_sp = float(volt_sp)
        self._check_trip()

    def set_curr_sp(self, curr_sp):
        self.curr_sp = float(curr_sp)
        self._check_trip()

    def set_overvolt(self,overvolt):
        self.overvolt = float(overvolt)
        self._check_trip()

    def set_overcurr(self,overcurr):
        self.overcurr = float(overcurr)
        self._check_trip()

    def set_output(self,output):
        self.output = output
        self._check_trip()

    def is_overcurrent_tripped(self):
        return self.ocp_tripped

    def is_overvolt_tripped(self):
        return self.ovp_tripped

    def _check_trip(self):
        if (self.output == 1):
            if (self.volt_sp > self.overvolt):
                self.output = 0
                self.ovp_tripped = True
            if(self.curr_sp > self.overcurr):
                self.output = 0
                self.ocp_tripped = True
