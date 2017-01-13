from lewis.adapters.stream import StreamAdapter, Cmd


class Keithley2400StreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    serial_commands = {
        Cmd("get_values", "^:READ\?$"),
        Cmd("reset", "^\*RST$"),
        Cmd("set_output_mode", "^\:OUTP\s(ON|OFF)$"),
        Cmd("get_output_mode", "^\:OUTP\?$"),
        Cmd("set_offset_compensation", "^\:SENS:RES:OCOM\s(ON|OFF)$"),
        Cmd("get_offset_compensation", "^\:SENS:RES:OCOM\?$"),
        Cmd("set_resistance_mode", "^\:SENS:RES:MODE\s(AUTO|MANUAL)$"),
        Cmd("get_resistance_mode", "^\:SENS:RES:MODE\?$"),
        Cmd("set_remote_sensing_mode", "^\:SYST:RSEN\s(ON|OFF)$"),
        Cmd("get_remote_sensing_mode", "^\:SYST:RSEN\?$"),
    }

    # Private control commands that can be used as an alternative to the lewis backdoor
    control_commands = {
    }

    commands = set.union(serial_commands, control_commands)

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def get_values(self):
        """ Get the current, voltage and resistance readings

        Returns:
            string : A string of 3 doubles: voltage, current, resistance. In that order
        """
        return ", ".join([
            self._device.get_voltage(as_string=True),
            self._device.get_current(as_string=True),
            self._device.get_resistance(as_string=True)
        ])

    def reset(self):
        """ Resets the device """
        self._device.reset()
        return "*RST"

    def _set_mode(self, set_method, command, new_mode, mode_lookup):
        set_method(mode_lookup[new_mode])
        return command + " " + str(new_mode)

    def _set_on_off(self, set_method, command, new_mode):
        return self._set_mode(set_method, command, new_mode, {"ON": True, "OFF": False})

    def _get_option(self, get_method, option_lookup):
        return option_lookup[get_method()]

    def _get_on_off(self, get_method):
        return self._get_option(get_method, {True: "ON", False: "OFF"})

    def _get_auto_manual(self, get_method):
        return self._get_option(get_method, {True: "AUTO", False: "MANUAL"})

    def set_output_mode(self, new_mode):
        return self._set_on_off(self._device.set_output_on, "OUTP:", new_mode)

    def get_output_mode(self):
        return self._get_on_off(self._device.output_is_on)

    def set_offset_compensation(self, new_mode):
        return self._set_on_off(self._device.set_offset_compensation_on, ":SENS:RES:OCOM", new_mode)


    def get_offset_compensation(self):
        return self._get_on_off(self._device.offset_compensation_is_on)

    def get_resistance_mode(self):
        return self._get_auto_manual(self._device.resistance_mode_is_auto)

    def set_resistance_mode(self, new_mode):
        return self._set_mode(self._device.set_resistance_mode_auto, ":SENS:RES:MODE", new_mode,
                              {"AUTO": True, "MANUAL": False})

    def get_remote_sensing_mode(self):
        return self._get_on_off(self._device.remote_sensing_is_on)

    def set_remote_sensing_mode(self, new_mode):
        return self._set_on_off(self._device.set_remote_sensing_on, ":SYST:RSEN", new_mode)

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)

