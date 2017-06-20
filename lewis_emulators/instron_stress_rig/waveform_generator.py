from waveform_generator_states import WaveformGeneratorStates as GenStates
from waveform_types import WaveformTypes
from quart_counter_actions import QuarterCycleCounterActions as QuartActions
from quart_counter_states import QuarterCycleCounterStates as QuartStates
from datetime import datetime, timedelta


class WaveformGenerator(object):
    STOP_DELAY = timedelta(seconds=3)

    def __init__(self):
        self.state = GenStates.STOPPED
        self.amplitude = 1.0
        self.frequency = 1.0
        self.type = WaveformTypes.SINE
        self.quart_action = QuartActions.NO_ACTION
        self.quart = 0
        self.quart_state = QuartStates.OFF
        self.stop_requested_at_time = None

    def abort(self):
        if self._active():
            self.state = GenStates.ABORTED
            self.stop_requested_at_time = None

    def finish(self):
        if self._active():
            self.stop_requested_at_time = datetime.now()
            self.state = GenStates.FINISHING

    def time_to_stop(self):
        print "Waveform generator state: " + str(self.state)
        return self.stop_requested_at_time is not None and \
               (datetime.now() - self.stop_requested_at_time) > WaveformGenerator.STOP_DELAY

    def stop(self):
        self.stop_requested_at_time = None
        self.state = GenStates.STOPPED

    def start(self):
        self.state = GenStates.RUNNING
        self.stop_requested_at_time = None

    def _active(self):
        return self.state in [GenStates.RUNNING, GenStates.HOLDING]

