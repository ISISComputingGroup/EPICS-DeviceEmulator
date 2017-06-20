from waveform_generator_states import WaveformGeneratorStates
from waveform_types import WaveformTypes
from quart_counter_actions import QuarterCycleCounterActions
from quart_counter_states import QuarterCycleCounterStates
from datetime import datetime, timedelta


class WaveformGenerator(object):
    STOP_DELAY = timedelta(seconds=3)

    def __init__(self):
        self.state = WaveformGeneratorStates.STOPPED
        self.amplitude = 1.0
        self.frequency = 1.0
        self.type = WaveformTypes.SINE
        self.quart_action = QuarterCycleCounterActions.NO_ACTION
        self.quart = 0
        self.quart_state = QuarterCycleCounterStates.OFF
        self.stop_requested_at_time = None

    def abort(self):
        self.state = WaveformGeneratorStates.ABORTED
        self.stop_requested_at_time = None

    def finish(self):
        self.stop_requested_at_time = datetime.now()
        self.state = WaveformGeneratorStates.FINISHING

    def time_to_stop(self):
        return self.stop_requested_at_time is not None and \
               (datetime.now() - self.stop_requested_at_time) > WaveformGenerator.STOP_DELAY

    def stop(self):
        self.stop_requested_at_time = None
        self.state = WaveformGeneratorStates.STOPPED

    def start(self):
        self.state = WaveformGeneratorStates.RUNNING
        self.stop_requested_at_time = None
