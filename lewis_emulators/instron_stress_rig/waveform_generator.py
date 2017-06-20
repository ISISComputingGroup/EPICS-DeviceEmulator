from waveform_generator_states import WaveformGeneratorStates
from waveform_types import WaveformTypes
from quart_counter_actions import QuarterCycleCounterActions
from quart_counter_states import QuarterCycleCounterStates
from multiprocessing import Pool
from time import sleep


class WaveformGenerator(object):
    def __init__(self):
        self.state = WaveformGeneratorStates.STOPPED
        self.amplitude = 1.0
        self.frequency = 1.0
        self.type = WaveformTypes.SINE
        self.quart_action = QuarterCycleCounterActions.NO_ACTION
        self.quart = 0
        self.quart_state = QuarterCycleCounterStates.OFF

    def abort(self):
        self.state = WaveformGeneratorStates.ABORTED

    def stop(self):
        def finish():
            self.state = WaveformGeneratorStates.STOPPED

        def wait_for_finish():
            time_to_finish = 3
            sleep(time_to_finish)

        if self.state in [WaveformGeneratorStates.RUNNING, WaveformGeneratorStates.HOLDING]:
            self.state = WaveformGeneratorStates.FINISHING
            Pool(processes=1).apply_async(wait_for_finish, [], finish)

    def start(self):
        self.state = WaveformGeneratorStates.RUNNING
