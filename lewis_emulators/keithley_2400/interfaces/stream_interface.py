from lewis.adapters.stream import StreamAdapter, Cmd
from ..control_modes import OutputMode


class Keithley2400StreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    serial_commands = {
        Cmd("get_values", "^:READ\?$"),
        Cmd("reset", "^\*RST$"),
        Cmd("identify", "^\*IDN?"),
        Cmd("set_output_mode", "^\:OUTP\s(1|0)$"),
        Cmd("get_output_mode", "^\:OUTP\?$"),
        Cmd("set_offset_compensation_mode", "^\:SENS:RES:OCOM\s(1|0)$"),
        Cmd("get_offset_compensation_mode", "^\:SENS:RES:OCOM\?$"),
        Cmd("set_resistance_mode", "^\:SENS:RES:MODE\s(AUTO|MAN)$"),
        Cmd("get_resistance_mode", "^\:SENS:RES:MODE\?$"),
        Cmd("set_remote_sensing_mode", "^\:SYST:RSEN\s(1|0)$"),
        Cmd("get_remote_sensing_mode", "^\:SYST:RSEN\?$"),
        Cmd("set_resistance_range_mode", "^\:SENS:RES:RANG:AUTO\s(0|1)$"),
        Cmd("get_resistance_range_mode", "^\:SENS:RES:RANG:AUTO\?$"),
        Cmd("set_resistance_range", "^\:SENS:RES:RANG\s([2][0]*)$"),
        Cmd("get_resistance_range", "^\:SENS:RES:RANG\?$"),
        Cmd("set_source_mode", "^\:SOUR:FUNC\s(CURR|VOLT)$"),
        Cmd("get_source_mode", "^\:SOUR:FUNC\?$"),
        Cmd("set_current_compliance", "^\:SENS:CURR:PROT\s([-+]?[0-9]*\.?[0-9]+)$"),
        Cmd("get_current_compliance", "^\:SENS:CURR:PROT\?$"),
        Cmd("set_voltage_compliance", "^\:SENS:VOLT:PROT\s([-+]?[0-9]*\.?[0-9]+)$"),
        Cmd("get_voltage_compliance", "^\:SENS:VOLT:PROT\?$"),
    }

    # Private control commands that can be used as an alternative to the lewis backdoor
    control_commands = {
        Cmd("set_voltage", "^\:_CTRL:VOLT\s([-+]?[0-9]*\.?[0-9]+)$"),
        Cmd("set_current", "^\:_CTRL:CURR\s([-+]?[0-9]*\.?[0-9]+)$"),
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
        ]) if self._device.get_output_mode() == OutputMode.ON else None

    def reset(self):
        """ Resets the device """
        self._device.reset()
        return "*RST"

    def identify(self):
        """ Replies with the device's identity """
        return "Keithley 2400 Source Meter emulator"

    def set_current(self, value):
        self._device.set_current(float(value))
        return "Current set to: " + str(value)

    def set_voltage(self, value):
        self._device.set_voltage(float(value))
        return "Voltage set to: " + str(value)

    def _set_mode(self, set_method, mode, command):
        """ The generic form of how mode sets are executed and responded to """
        set_method(mode)
        return command + " " + mode

    def set_output_mode(self, new_mode):
        return self._set_mode(self._device.set_output_mode, new_mode, "OUTP:")

    def get_output_mode(self):
        return self._device.get_output_mode()

    def set_offset_compensation_mode(self, new_mode):
        return self._set_mode(self._device.set_offset_compensation_mode, new_mode, ":SENS:RES:OCOM")

    def get_offset_compensation_mode(self):
        return self._device.get_offset_compensation_mode()

    def set_resistance_mode(self, new_mode):
        return self._set_mode(self._device.set_resistance_mode, new_mode, ":SENS:RES:MODE")

    def get_resistance_mode(self):
        return self._device.get_resistance_mode()

    def set_remote_sensing_mode(self, new_mode):
        return self._set_mode(self._device.set_remote_sensing_mode, new_mode, ":SYST:RSEN")

    def get_remote_sensing_mode(self):
        return self._device.get_remote_sensing_mode()

    def set_resistance_range_mode(self, new_mode):
        return self._set_mode(self._device.set_resistance_range_mode, new_mode, ":SENS:RES:RANG:AUTO")

    def get_resistance_range_mode(self):
        return self._device.get_resistance_range_mode()

    def set_resistance_range(self, value):
        return self._device.set_resistance_range(int(value))

    def get_resistance_range(self):
        return self._device.get_resistance_range()

    def set_source_mode(self, new_mode):
        return self._set_mode(self._device.set_source_mode, new_mode, ":SOUR:FUNC")

    def get_source_mode(self):
        return self._device.get_source_mode()

    def set_current_compliance(self, value):
        return self._device.set_current_compliance(float(value))

    def get_current_compliance(self):
        return self._device.get_current_compliance()

    def set_voltage_compliance(self, value):
        return self._device.set_voltage_compliance(float(value))

    def get_voltage_compliance(self):
        return self._device.get_voltage_compliance()

    def handle_error(self, request, error):
        print  "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

