from lewis.adapters.stream import StreamAdapter, Cmd


class InstronStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_control_channel", "^Q300$"),
        Cmd("set_control_channel", "^C300,([1-3])$"),
        Cmd("get_watchdog_status", "^Q904$"),
        Cmd("set_watchdog_status", "^C904,([0-2]),([0-3])$"),
        Cmd("get_control_mode", "^Q909$"),
        Cmd("set_control_mode", "^P909,([0-1])$"),
        Cmd("get_status", "^Q22$"),
        Cmd("arbitrary_command", "^([a-z]*)$"),
        Cmd("get_actuator_status", "^Q23$"),
        Cmd("set_actuator_status", "^C23,([0-1])$"),
        Cmd("get_movement_type", "^Q1$"),
        Cmd("set_movement_type", "^C1,([0-3])$"),
        Cmd("get_step_time", "^Q86,([1-3])$"),
        Cmd("set_step_time", "^C86,([1-3]),([0-9]*.[0-9]*)$"),
        Cmd("get_chan_waveform_type", "^Q2,([1-3])$"),
        Cmd("set_chan_waveform_type", "^C2,([1-3]),([0-5])$"),
        Cmd("get_ramp_amplitude_setpoint", "^Q4,([1-3])$"),
        Cmd("set_ramp_amplitude_setpoint", "^C4,([1-3]),([0-9]*.[0-9]*)$"),
        Cmd("get_single_point_feedback_data", "^Q134,([1-3]),([0-9]+)$"),
        Cmd("get_chan_scale", "^Q308,([1-3])$"),
        Cmd("get_strain_channel_length", "^Q340,([1-3])$"),
        Cmd("get_chan_area", "^Q341,([1-3])$"),
        Cmd("set_chan_area", "^C341,([1-3]),([0-9]*.[0-9]*)$"),
        Cmd("get_chan_type", "^Q307,([1-3])$"),
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_control_channel(self):
        return self._device.get_control_channel()

    def set_control_channel(self, channel):
        self._device.set_control_channel(int(channel))

    def get_watchdog_status(self):
        enabled, status = self._device.get_watchdog_status()
        return "{},{}".format(enabled, status)

    def set_watchdog_status(self, cv1, cv2):
        self._device.set_watchdog_status(int(cv1), int(cv2))

    def get_control_mode(self):
        return self._device.get_control_mode()

    def set_control_mode(self, mode):
        self._device.set_control_mode(int(mode))

    def get_status(self):
        return int(self._device.get_status())

    def arbitrary_command(self, command):
        return "Arb_com_response_" + str(command)

    def get_actuator_status(self):
        return self._device.get_actuator_status()

    def set_actuator_status(self, mode):
        self._device.set_actuator_status(int(mode))

    def get_movement_type(self):
        return self._device.get_movement_type()

    def set_movement_type(self, mov_type):
        self._device.set_movement_type(int(mov_type))

    def get_step_time(self, channel):
        return float(self._device.get_step_time(int(channel)))

    def set_step_time(self, channel, value):
        self._device.set_step_time(int(channel), float(value))

    def get_chan_waveform_type(self, channel):
        return int(self._device.get_chan_waveform_type(int(channel)))

    def set_chan_waveform_type(self, channel, value):
        self._device.set_chan_waveform_type(int(channel), int(value))

    def get_ramp_amplitude_setpoint(self, channel):
        return float(self._device.get_ramp_amplitude_setpoint(int(channel)))

    def set_ramp_amplitude_setpoint(self, channel, value):
        self._device.set_ramp_amplitude_setpoint(int(channel), float(value))

    def get_single_point_feedback_data(self, channel, type):
        return float(self._device.get_chan_value(int(channel), int(type)))

    def get_chan_scale(self, channel):
        return self._device.get_chan_scale(int(channel))

    def get_strain_channel_length(self, channel):
        return self._device.get_strain_channel_length(int(channel))

    def get_chan_area(self, channel):
        return self._device.get_chan_area(int(channel))

    def set_chan_area(self, channel, value):
        self._device.set_chan_area(int(channel), float(value))

    def get_chan_type(self, channel):
        transducer_type = self._device.get_chan_transducer_type(int(channel))
        chan_type = self._device.get_chan_type(int(channel))
        return "{a},{b}".format(a=transducer_type, b=chan_type)
