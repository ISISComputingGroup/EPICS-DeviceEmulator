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

    def _set_on_off(self, set_method, type_string, command, new_mode):
        if new_mode == "ON":
            set_method(True)
        elif new_mode == "OFF":
            set_method(False)
        else:
            raise Exception("Invalid " + type_string + " " + str(new_mode))
        return command + " " + str(new_mode)

    def _get_on_off(self, get_method):
        if get_method():
            return "ON"
        else:
            return "OFF"

    def set_output_mode(self, new_mode):
        return self._set_on_off(self._device.set_output_on, "output mode", "OUTP:", new_mode)

    def get_output_mode(self):
        return self._get_on_off(self._device.output_is_on)

    def set_offset_compensation(self, new_mode):
        return self._set_on_off(self._device.set_offset_compensation_on, "offset compensation mode",
                         ":SENS:RES:OCOM", new_mode)

    def get_offset_compensation(self):
        return self._get_on_off(self._device.offset_compensation_is_on)

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)

