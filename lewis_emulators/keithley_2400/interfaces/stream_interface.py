from lewis.adapters.stream import StreamInterface, Cmd
from ..control_modes import OutputMode
from lewis.core.logging import has_log


@has_log
class Keithley2400StreamInterface(StreamInterface):

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
        Cmd("set_resistance_range", "^\:SENS:RES:RANG\s([-+]?[0-9]*\.?[0-9]+)$"),
        Cmd("get_resistance_range", "^\:SENS:RES:RANG\?$"),
        Cmd("set_source_mode", "^\:SOUR:FUNC\s(CURR|VOLT)$"),
        Cmd("get_source_mode", "^\:SOUR:FUNC\?$"),
        Cmd("set_current_compliance", "^\:SENS:CURR:PROT\s([-+]?[0-9]*\.?[0-9]+)$"),
        Cmd("get_current_compliance", "^\:SENS:CURR:PROT\?$"),
        Cmd("set_voltage_compliance", "^\:SENS:VOLT:PROT\s([-+]?[0-9]*\.?[0-9]+)$"),
        Cmd("get_voltage_compliance", "^\:SENS:VOLT:PROT\?$"),
        Cmd("set_source_voltage", "^\:SOUR:VOLT:LEV\s([-+]?[0-9]*\.?[0-9]+)$"),
        Cmd("get_source_voltage", "^\:SOUR:VOLT:LEV\?$"),
        Cmd("set_source_current", "^\:SOUR:CURR:LEV\s([-+]?[0-9]*\.?[0-9]+)$"),
        Cmd("get_source_current", "^\:SOUR:CURR:LEV\?$"),
        Cmd("set_source_current_autorange_mode", "^\:SOUR:CURR:RANG:AUTO\s(1|0)$"),
        Cmd("get_source_current_autorange_mode", "^\:SOUR:CURR:RANG:AUTO\?$"),
        Cmd("set_source_voltage_autorange_mode", "^\:SOUR:VOLT:RANG:AUTO\s(1|0)$"),
        Cmd("get_source_voltage_autorange_mode", "^\:SOUR:VOLT:RANG:AUTO\?$"),
        Cmd("get_source_current_range", "^\:SOUR:CURR:RANG\?$"),
        Cmd("set_source_current_range", "^\:SOUR:CURR:RANG\s([-+]?[0-9]*\.?[0-9]+)$"),
        Cmd("get_source_voltage_range", "^\:SOUR:VOLT:RANG\?$"),
        #Cmd("set_source_voltage_range", "^\:SOUR:VOLT:RANG\s([-+]?[0-9]*\.?[0-9]+)$"),
        Cmd("set_source_voltage_range", "^\:SOUR:VOLT:RANG\s([-+]?[0-9]*\.?[0-9]+e?-?[0-9]+?)$"),
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
        """
        Get the current, voltage and resistance readings

        :return: A string of 3 doubles: voltage, current, resistance. In that order
        """
        return ", ".join([
            self._device.get_voltage(as_string=True),
            self._device.get_current(as_string=True),
            self._device.get_resistance(as_string=True)
        ]) if self._device.get_output_mode() == OutputMode.ON else None

    def reset(self):
        """
        Resets the device.
        """
        self._device.reset()
        return "*RST"

    def identify(self):
        """
        Replies with the device's identity.
        """
        return "Keithley 2400 Source Meter emulator"

    def set_current(self, value):
        self._device.set_current(float(value))
        return "Current set to: " + str(value)

    def set_voltage(self, value):
        self._device.set_voltage(float(value))
        return "Voltage set to: " + str(value)

    def _set_mode(self, set_method, mode, command):
        """
        The generic form of how mode sets are executed and responded to.
        """
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
        return self._device.set_resistance_range(float(value))

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

    def set_source_voltage(self, value):
        return self._device.set_source_voltage(float(value))

    def get_source_voltage(self):
        return self._device.get_source_voltage()

    def set_source_current(self, value):
        return self._device.set_source_current(float(value))

    def get_source_current(self):
        return self._device.get_source_current()

    def get_source_current_autorange_mode(self):
        return self._device.get_source_current_autorange_mode()

    def set_source_current_autorange_mode(self, value):
        return self._device.set_source_current_autorange_mode(value)

    def get_source_voltage_autorange_mode(self):
        return self._device.get_source_voltage_autorange_mode()

    def set_source_voltage_autorange_mode(self, value):
        return self._device.set_source_voltage_autorange_mode(value)

    @has_log
    def handle_error(self, request, error):
        err = "An error occurred at request {}: {}".format(str(request), str(error))
        print(err)
        self.log.info(err)
        return str(err)

    def set_source_current_range(self, value):
        return self._device.set_source_current_range(float(value))

    def get_source_current_range(self):
        return self._device.get_source_current_range()

    @has_log
    def set_source_voltage_range(self, value):
        self.log.info("Setting value to {:16f}".format(float(value)))

        val = self._device.set_source_voltage_range(float(value))

        self.log.info("Set value to {:16f}".format(float(self._device._source_voltage_range)))

        return val

    @has_log
    def get_source_voltage_range(self):
        val = self._device.get_source_voltage_range()
        self.log.info("Getting value {}".format(val))
        return val

