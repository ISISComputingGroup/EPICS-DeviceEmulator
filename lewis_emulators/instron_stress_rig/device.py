from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice

import time


class SimulatedInstron(StateMachineDevice):

    def _initialize_data(self):
        """ Initialize all of the device's attributes """

        # When initialisation is complete, this is set to true and the device will enter a running state
        self.ready = True
        self._control_channel = 1
        self._watchdog_status = (0, 0)
        self._control_mode = 0
        self._actuator_status = 0
        self._movement_type = 2
        self.current_time = 0
        self.watchdog_refresh_time = 0

        # Mode 0 = Ramp waveform
        # Mode 1 = Random waveform
        self._waveform_mode = 0


    def raise_exception_if_cannot_write(self):
        if self._control_mode != 1:
            raise Exception("Not in the correct control mode to execute that command!")

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])

    def get_control_channel(self):
        return self._control_channel

    def set_control_channel(self, channel):
        self._control_channel = channel

    def get_watchdog_status(self):
        return self._watchdog_status

    def set_watchdog_status(self, enabled, status):
        self._watchdog_status = (enabled, status)
        self.watchdog_refresh_time = self.current_time

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
        if status == 0:
            self._movement_type = 0

    def get_movement_type(self):
        return self._movement_type

    def set_movement_type(self, mov_type):
        self.raise_exception_if_cannot_write()

        if self._waveform_mode == 0:
            self._movement_type = mov_type
        else:
            self._movement_type = mov_type + 3

    def set_current_time(self):
        self.current_time = time.time()

