from collections import OrderedDict
from states import DefaultInitState, DefaultStoppedState, DefaultStartedState
from lewis.devices import StateMachineDevice
from chopper_type import ChopperType


class SimulatedMk2Chopper(StateMachineDevice):

    # Dictionary of valid (frequencies, max phase delay) for each chopper type: 50Hz/100Hz
    CHOPPER_TYPES = [ChopperType(50,  [5, 10, 12.5, 16.67, 25, 50]), ChopperType(100, [12.5, 25, 50, 100])]

    def _initialize_data(self):
        """ Initialize all of the device's attributes """
        self._type = SimulatedMk2Chopper.CHOPPER_TYPES[0]

        self._demanded_frequency, self._max_phase_delay = self._type.valid_states[-1]
        self._true_frequency = 0

        self._demanded_phase_delay = 0
        self._true_phase_delay = 0

        self._demanded_phase_error_window = 0
        self._true_phase_error = 0

        self._started = False

        # When initialisation is complete, this is set to true and the device will enter a running state
        self.ready = True

    def _get_state_handlers(self):
        return {
            'init': DefaultInitState(),
            'stopped': DefaultStoppedState(),
            'started': DefaultStartedState(),
        }

    def _get_initial_state(self):
        return 'init'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('init', 'stopped'), lambda: self.ready),
            (('stopped', 'started'), lambda: self._started is True),
            (('started', 'stopped'), lambda: self._started is False),
        ])

    def get_demanded_frequency(self):
        return self._demanded_frequency

    def get_true_frequency(self):
        return self._true_frequency

    def get_demanded_phase_delay(self):
        return self._demanded_phase_delay

    def get_true_phase_delay(self):
        return self._true_phase_delay

    def get_demanded_phase_error_window(self):
        return self._demanded_phase_error_window

    def get_true_phase_error(self):
        return self._true_phase_error

    def set_demanded_frequency(self, new_frequency_int):
        try:
            self._demanded_frequency, self._max_phase_delay = next((f, p) for f, p in self._type.valid_states if
                                                                   int(f)==int(new_frequency_int))
        except StopIteration:
            # No value found, do nothing
            pass

    def set_demanded_phase_delay(self, new_phase_delay):
        self._demanded_phase_delay = min(new_phase_delay, self._max_phase_delay)

    def set_true_frequency(self, new_frequency):
        self._true_frequency = new_frequency

    def set_chopper_type(self, frequency):
        try:
            self._type = next(ct for ct in SimulatedMk2Chopper.CHOPPER_TYPES if ct.system_frequency == frequency)
        except StopIteration:
            # The new type wasn't valid, do nothing
            pass
        else:
            # Make sure the demanded frequency is a valid frequency for the new type
            self.set_frequency(min(self._type.valid_frequencies, key=lambda x:abs(x - self._demanded_frequency)))

    def start(self):
        self._started = True

    def stop(self):
        self._started = False