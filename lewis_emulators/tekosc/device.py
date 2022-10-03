from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


class SourceChannel:
    def __init__(self, channel):
        self.preamble = f':WFMOUTPRE:BYT_NR 1;BIT_NR 8;ENCDG ASCII;BN_FMT RI;BYT_OR MSB; \
        WFID "Ch{channel}, DC coupling, 100.0mV/div, 4.000us/div, 10000 points, Sample mode";   \
        NR_PT 20;PT_FMT Y;XUNIT "s";XINCR 4.0000E-9;XZERO -20.0000E-6;PT_OFF 0;         \
        YUNIT "V";YMULT 4.0000E-3;YOFF 0.0000;YZERO 0.0000;'
        self.curve = f":CURVe {channel},1,4,2,4,3,0,3,3,3,3,3,3,4,3,5,6,6,7,3"

    def get_waveform(self):
        return self.preamble + self.curve


class SimulatedTekOsc(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.channels = {1: SourceChannel(1), 2: SourceChannel(2)}
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

