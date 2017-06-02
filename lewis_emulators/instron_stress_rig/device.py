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
        self.status = 7680

        # Mode 0 = Ramp waveform
        # Mode 1 = Random waveform
        self._waveform_mode = 0

        # Maps a channel number to a channel object
        # Usually 1=position, 2=stress, 3=strain but in the
        # context of the emulator it doesn't matter as all channels are treated equally.
        self.channels = {1 : Channel(), 2 : Channel(), 3 : Channel()}

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

    def get_status(self):
        return self.status

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

    def set_step_time(self, channel, value):
        self.channels[channel].step_time = value

    def get_step_time(self, channel):
        return self.channels[channel].step_time

    def set_chan_waveform_type(self, channel, value):
        self.channels[channel].waveform_type = value

    def get_chan_waveform_type(self, channel):
        return self.channels[channel].waveform_type

    def set_ramp_amplitude_setpoint(self, channel, value):
        self.channels[channel].ramp_amplitude_setpoint = value

    def get_ramp_amplitude_setpoint(self, channel):
        return self.channels[channel].ramp_amplitude_setpoint

    def get_chan_scale(self, channel):
        return self.channels[channel].chan_scale

class Channel(object):
    def __init__(self):
        self.waveform_type = 0
        self.step_time = 0
        self.ramp_amplitude_setpoint = 0
        self.chan_scale = 10

