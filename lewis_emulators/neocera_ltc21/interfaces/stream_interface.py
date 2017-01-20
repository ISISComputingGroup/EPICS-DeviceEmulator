import re

from lewis.adapters.stream import StreamAdapter, Cmd

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
    for arg in args:
        args_regex += "{stripped}({arg})".format(arg=arg, stripped=r"[\r\n\s]*")

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
        sensor_index = int(sensor_number) - 1
        try:
            temp = self._device.temperature[sensor_index]
            unit = self._device.unit[sensor_index]
            if temp is None:
                return " ------ "
            return "{0:8f}{1:1s}".format(temp, unit)
        except (IndexError, ValueError, TypeError):
            print "Error: invalid sensor number requested '{0}'".format(sensor_number)
            self._device.error = NeoceraDeviceErrors(NeoceraDeviceErrors.BAD_PARAMETER)
            return ""

    def handle_error(self, request, error):
        """

        Handles errors.

        Args:
            request:
            error:

        """
        print "An error occurred at request " + repr(request) + ": " + repr(error)

