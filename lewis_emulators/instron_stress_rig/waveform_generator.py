from waveform_generator_states import WaveformGeneratorStates
from waveform_types import WaveformTypes
from quart_counter_actions import QuarterCycleCounterActions
from quart_counter_states import QuarterCycleCounterStates

class WaveformGenerator(object):
    def __init__(self):
        self.state = WaveformGeneratorStates.STOPPED
        self.amplitude = 1.0
        self.frequency = 1.0
        self.type = WaveformTypes.SINE
        self.quart_action = QuarterCycleCounterActions.NO_ACTION
        self.quart = 0
        self.quart_state = QuarterCycleCounterStates.OFF

