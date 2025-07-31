from collections import OrderedDict

from lewis.devices import StateMachineDevice
from lewis.core.statemachine import State

from .states import DefaultState

class SimulatedOPCUA(StateMachineDevice):
    """Class representing a simulated OPC UA PLC.
    """

    #Need a dictionary ? of some sort to store PV values and their
    #corresponding address/name on the OPCUA server. Also need
    #IP address and other server info, and possibly library to start
    #the server... 

    def _get_state_handlers(self):
        return super()._get_state_handlers()
    
    def _get_initial_state(self):
        return super()._get_initial_state()
    
    def _get_transition_handlers(self):
        return super()._get_transition_handlers()