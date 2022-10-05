from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


class SourceChannel:
    def __init__(self, channel):
        # Preamble elements
        self.x_increment = channel*2+1
        self.y_multiplier = channel*2
        self.x_unit = "\"s\""
        self.y_unit = "\"V\""

        self.curve = f"{channel},1,4,2,4,3,0,3,3,3,3,3,3,4,3,5,6,6,7,3"

    def get_waveform(self):
        return self.preamble + self.curve


class SimulatedTekOsc(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.channels = {
            1: SourceChannel(1), 
            2: SourceChannel(2),
            3: SourceChannel(3),
            4: SourceChannel(4),
        }
        self.triggered = False

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

