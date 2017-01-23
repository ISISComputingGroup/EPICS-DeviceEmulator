import re

from lewis.adapters.stream import StreamAdapter, Cmd

from lewis_emulators.neocera_ltc21.constants import HEATER_INDEX, CONTROL_TYPE_MAX, CONTROL_TYPE_MIN, ANALOG_INDEX
from lewis_emulators.neocera_ltc21.device_errors import NeoceraDeviceErrors
from lewis_emulators.neocera_ltc21.states import MonitorState, ControlState


def get_regex(command, *args):

    """

    Takes a command and optional arguments and turns then into a regex for lewis

    Args:
        command: the command to turn into a regex

    Returns: a regex for lewis

    """

    command = re.escape(command)
    args_regex = ""
    comma = ""
    for arg in args:
        args_regex += "{stripped}{comma}({arg})".format(arg=arg, stripped=r"[\r\n\s]*", comma=comma)
        comma = ","

    return "{stripped}{command}{args_regex}{stripped}".format(
        stripped=r"[\r\n\s]*", args_regex=args_regex, command=command)


class NeoceraStreamInterface(StreamAdapter):
    """
    Stream interface for the serial port
    """

    commands = {
        Cmd("get_state", get_regex("QISTATE?")),
        Cmd("set_state_monitor", get_regex("SMON")),
        Cmd("set_state_control", get_regex("SCONT")),
        Cmd("get_temperature_and_unit", get_regex("QSAMP?", "\d")),
        Cmd("get_setpoint_and_unit", get_regex("QSETP?", "\d")),
        Cmd("set_setpoint", get_regex("SETP", "\d", "[+-]?\d+\.?\d*")),
        Cmd("get_output_config", get_regex("QOUT?", "\d")),
        Cmd("set_heater_control", get_regex("SHCONT", "\d")),
        Cmd("set_analog_control", get_regex("SACONT", "\d")),
        Cmd("get_heater", get_regex("QHEAT?")),
    }

    in_terminator = ";"
    out_terminator = ";\n"

    def get_state(self):

        """
        Gets the current state of the device

        Returns: a single character string containing a number which represents the state of the device

        """

        if self._device.state == MonitorState.NAME:
            return "0"
        elif self._device.state == ControlState.NAME:
            return "1"

    def get_temperature_and_unit(self, sensor_number):
        """
        Return the temperature and unit for the sensor number given.
        Args:
            sensor_number: sensor number

        Returns: formatted temperature and unit for the device

        """
        return self._get_indexed_value_with_unit(self._device.temperatures, sensor_number)

    def _get_indexed_value_with_unit(self, device_values, item_number):
        """
        Get a temperature like value back from device temperatures in the format produced by the device
        Args:
            device_values: device value, e.g. temperatures list
            item_number: item to return

        Returns: temp and units; e.g. setpoint 1.2K

        """
        try:
            sensor_index = int(item_number) - 1
            device_value = device_values[sensor_index]

            # for temperatures it can not read
            if device_value is None:
                return " ------ "

            unit = self._device.units[sensor_index]

            return "{0:8f}{1:1s}".format(device_value, unit)

        except (IndexError, ValueError, TypeError):
            print "Error: invalid sensor number requested '{0}'".format(item_number)
            self._device.error = NeoceraDeviceErrors(NeoceraDeviceErrors.BAD_PARAMETER)
            return ""

    def get_setpoint_and_unit(self, output_number):
        """

        Args:
            output_number: the number of set point top return; 1=HEATER, 2=ANALOG

        Returns: setpoint with unit

        """
        return self._get_indexed_value_with_unit(self._device.setpoints, output_number)

    def set_setpoint(self, output_number, value):
        """
        Set the setpoint.
        Args:
            output_number: output number; 1=HEATER, 2=ANALOG
            value: value to set it to

        Returns: blank

        """
        try:
            output_index = int(output_number) - 1
            setpoint = float(value)

            self._device.setpoints[output_index] = setpoint
        except (IndexError, ValueError, TypeError):
            print "Error: invalid output number, '{0}', or setpoint value, '{1}'".format(output_number, value)
            self._device.error = NeoceraDeviceErrors(NeoceraDeviceErrors.BAD_PARAMETER)
            return ""

    def get_output_config(self, output_number):
        """
        Reply to output configuration query.
            # Example QOUT?1;   produces -> 2;4;3;
            # Example QOUT?2;   produces -> 3;5;

        Args:
            output_number: The output number being querries; 1 HEATER, 2 Analogue

        Returns: configuration as a string; sensor source;control;heater_range

        """

        device = self._device
        try:
            output_index = int(output_number) - 1

            output_config = "{sensor_source};{control}".format(
                sensor_source=device.sensor_source[output_index], control=device.control[output_index])

            if output_index == HEATER_INDEX:
                output_config += ";{heater_range}".format(heater_range=device.heater_range)

            return output_config

        except (IndexError, ValueError, TypeError):
            print "Error: invalid output number, '{0}'".format(output_number)
            device.error = NeoceraDeviceErrors(NeoceraDeviceErrors.BAD_PARAMETER)
            return ""

    def set_heater_control(self, control_type_number):
        """
        Set the heater output control
        Args:
            control_type_number: control type to set the heater to

        Returns: None

        """

        self._set_output_control(HEATER_INDEX, control_type_number)

    def set_analog_control(self, control_type_number):
        """
        Set the analog output control
        Args:
            control_type_number: control type to set the heater to

        Returns: None

        """

        self._set_output_control(ANALOG_INDEX, control_type_number)

    def _set_output_control(self, output_index, control_type_number):
        """
        Set the output control for either the heater or the analog output
        Args:
            output_index: output index
            control_type_number: control type to set

        Returns: None

        """
        device = self._device
        try:
            control_type = int(control_type_number)

            if control_type < CONTROL_TYPE_MIN[output_index] or \
                    control_type > CONTROL_TYPE_MAX[output_index]:
                raise ValueError("Bad control type number")

            self._device.control[output_index] = control_type

        except (IndexError, ValueError, TypeError):
            print "Error: invalid control type number for output {output}, '{0}'".format(
                control_type_number, output=output_index)
            device.error = NeoceraDeviceErrors(NeoceraDeviceErrors.BAD_PARAMETER)

    def get_heater(self):
        """

        Returns: Heater output

        """
        return "{0:5.1f}".format(self._device.heater)

    def handle_error(self, request, error):
        """

        Handles errors.

        Args:
            request:
            error:

        """
        print "An error occurred at request " + repr(request) + ": " + repr(error)
