from collections import OrderedDict
from states import DefaultInitState, DefaultStoppedState, DefaultStartedState
from lewis.devices import StateMachineDevice


class SimulatedInstron(StateMachineDevice):

    def _initialize_data(self):
        """ Initialize all of the device's attributes """


        # When initialisation is complete, this is set to true and the device will enter a running state
        self.ready = True
        self._control_channel = 0

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

    def get_control_channel(self):
        return self._control_channel
		
    def set_control_channel(self, channel):
        self._control_channel = channel

    def start(self):
        self._started = True

    def stop(self):
        self._started = False
