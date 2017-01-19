import re

from lewis.adapters.stream import StreamAdapter, Cmd
from lewis_emulators.neocera_ltc21.states import MonitorState, ControlState


def get_regex(arg):

    """

    Takes a command and turns it into a regex for lewis

    Args:
        arg: the command to turn into a regex

    Returns: a regex for lewis

    """

    arg = re.escape(arg)
    output = r"[\r\n]*" + arg + r"[\r\n]*"
    return output


class NeoceraStreamInterface(StreamAdapter):

    commands = {
        Cmd("get_state", get_regex("QISTATE?")),
        Cmd("set_state_monitor", get_regex("SMON")),
        Cmd("set_state_control", get_regex("SCONT")),
        Cmd("get_temperature_and_unit", get_regex("QSAMP?1")),
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

    def get_temperature_and_unit(self):
        return "{0:10f}{1:1s}".format(self._device.temperature, self._device.unit)

    def handle_error(self, request, error):
        """

        Handles errors.

        Args:
            request:
            error:

        """
        print "An error occurred at request " + repr(request) + ": " + repr(error)

