from waveform_generator_states import WaveformGeneratorStates as GenStates
from waveform_types import WaveformTypes
from datetime import datetime, timedelta
from quarter_cycle_event_detector import QuarterCycleEventDetector as QCED


class WaveformGenerator(object):
    STOP_DELAY = timedelta(seconds=3)

    def __init__(self):
        self.state = GenStates.STOPPED
        self.amplitude = {i+1: 0.0 for i in range(3)}
        self.frequency = {i+1: 0.0 for i in range(3)}
        self.type = {i+1: WaveformTypes.SINE for i in range(3)}
        self.stop_requested_at_time = None
        self.quart_counter = QCED()

    def abort(self):
        if self._active():
            self.state = GenStates.ABORTED
            self.stop_requested_at_time = None

    def finish(self):
        if self._active():
            self.stop_requested_at_time = datetime.now()
            self.state = GenStates.FINISHING

    def time_to_stop(self):
        return self.stop_requested_at_time is not None and \
               (datetime.now() - self.stop_requested_at_time) > WaveformGenerator.STOP_DELAY

    def stop(self):
        self.stop_requested_at_time = None
        self.state = GenStates.STOPPED

    def start(self):
        self.state = GenStates.RUNNING
        self.stop_requested_at_time = None
        self.quart_counter.start()

    def _active(self):
        return self.state in [GenStates.RUNNING, GenStates.HOLDING]
