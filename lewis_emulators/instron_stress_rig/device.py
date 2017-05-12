from collections import OrderedDict
from states import DefaultInitState, DefaultStoppedState, DefaultStartedState
from lewis.devices import StateMachineDevice


class SimulatedInstron(StateMachineDevice):

    def _initialize_data(self):
        """ Initialize all of the device's attributes """

        # When initialisation is complete, this is set to true and the device will enter a running state
        self.ready = True
        self._control_channel = 0
        self._watchdog_status = (0, 0)
        self._control_mode = 0
        self._actuator_status = 0

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

    def get_watchdog_status(self):
        return self._watchdog_status

    def set_watchdog_status(self, enabled, status):
        self._watchdog_status = (enabled, status)

    def get_control_mode(self):
        return self._control_mode

    def set_control_mode(self, mode):
        self._control_mode = mode

    def start(self):
        self._started = True

    def stop(self):
        self._started = False

    def get_actuator_status(self):
        return self._actuator_status

    def set_actuator_status(self, status):
        print "Actuator status was " + str(self._actuator_status)
        self._actuator_status = int(status)
        print "Now it is " + str(status)
