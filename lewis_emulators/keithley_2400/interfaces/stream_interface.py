from lewis.adapters.stream import StreamAdapter, Cmd


class Keithley2400StreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    serial_commands = {
        Cmd("get_values", "^:READ\?$"),
        Cmd("reset", "^\*RST$"),
        Cmd("set_output_mode", "^\:OUTP\s(ON|OFF)$"),
        Cmd("get_output_mode", "^\:OUTP\?$"),
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

    def set_output_mode(self, new_mode):
        if new_mode == "ON":
            self._device.set_output_on(True)
        elif new_mode == "OFF":
            self._device.set_output_on(False)
        else:
            raise Exception("Invalid output mode received: " + str(new_mode))
        return ":OUTP " + str(new_mode)

    def get_output_mode(self):
        if self._device.output_is_on():
            return "ON"
        else:
            return "OFF"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)

