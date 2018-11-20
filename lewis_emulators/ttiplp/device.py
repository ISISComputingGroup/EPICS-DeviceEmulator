from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedTtiplp(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.ident="THURLBY THANDAR, PL303-P, 490296, 3.02-4.06"
        self.volt=0
        self.volt_sp=0
        self.curr=0
        self.curr_sp=0
        self.output=0
        self.overvolt=0
        self.overcurr=0
        
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
        
    def set_volt_sp(self, volt_sp):
        if float(volt_sp)>float(self.overvolt):
            self.output=0
            self.volt=0
            self.curr=0

