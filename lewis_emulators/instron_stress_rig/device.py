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
        self._movement_type = 2

    def raise_exception_if_cannot_write(self):
        if int(self._control_mode) != int(1):
            raise Exception("Not in the correct control mode to execute that command! Current control mode is " + str(self._control_mode))

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
        self.raise_exception_if_cannot_write()
        self._actuator_status = int(status)

    def get_movement_type(self):
        return self._movement_type

    def set_movement_type(self, mov_type):
        self.raise_exception_if_cannot_write()
        self._movement_type = mov_type
