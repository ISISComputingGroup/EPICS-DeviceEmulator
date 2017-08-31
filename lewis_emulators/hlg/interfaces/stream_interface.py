from lewis.adapters.stream import StreamAdapter
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder

PREFIXES = [
    "",  # 0
    "\r\n",  # 1
    "\r\n  ",  # 2
    "\r\n01:23:45 ",  # 3
    "\r\n -------> ",  # 4
    ", ",  # 5
]


@has_log
class HlgStreamInterface(StreamAdapter):
    """
    Stream interface for the serial port
    """

    commands = {
        CmdBuilder("get_level").escape("PM").build(),
        CmdBuilder("set_verbosity").escape("CV").int().build(),
        CmdBuilder("set_prefix").escape("CP").int().build()
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def set_verbosity(self, verbosity):
        """
        Set the verbosity of the output from the device

        Args:
            verbosity: 0 normal, 1 labview style (more verbose)

        Returns: confirmation message

        """
        verbosity_as_int = int(verbosity)
        if verbosity_as_int != 0 and verbosity_as_int != 1:
            raise AssertionError("Verbosity must be 0 or 1 was '{0}'".format(verbosity))
        self._device.verbosity = verbosity_as_int
        if verbosity_as_int == 0:
            out_verbose = "Normal"
        else:
            out_verbose = "labVIEW"
        return self._format_output("CV{0}".format(verbosity_as_int), "Verbose=", out_verbose)

    def set_prefix(self, prefix):
        """
        Set the prefix the device returns
        Args:
            prefix: prefix id 0-5 see PREFIXES for details

        Returns: confirmation message

        """
        prefix_as_int = int(prefix)
        if prefix_as_int < 0 or prefix_as_int >= len(PREFIXES):
            raise AssertionError("Prefix must be between 0 and 5 '{0}'".format(prefix))
        self._device.prefix = prefix_as_int
        return self._format_output("CP{0}".format(prefix_as_int), "Verbose=", prefix)

    def get_level(self):

        """
        Gets the current level

        Returns: level in correct units

        """
        if self._device.level is None:
            return None
        else:
            return self._format_output("PM", "Probe value=", "{level:.3f} mm".format(level=self._device.level))

    def _format_output(self, echo, verbose_prefix, data):
        """
        Format the output of a command depending on verbosity and prefix settings of device
        Args:
            echo: string to echo back to user
            verbose_prefix: prefix for value in normal verbose mode
            data: data to output

        Returns: formatted output from command

        """
        output_string = echo
        output_string += PREFIXES[self._device.prefix]
        if self._device.verbosity == 0:
            output_string += verbose_prefix
        output_string += data
        return output_string
