from lewis.adapters.stream import StreamAdapter
from lewis_emulators.utils.command_builder import CmdBuilder


class CybamanStreamInterface(StreamAdapter):
    """
    Stream interface for the serial port
    """

    commands = {
    }

    in_terminator = "\r"
    out_terminator = ""

    def handle_error(self, request, error):
        """
        If command is not recognised print and error.

        :param request: requested string
        :param error: problem
        :return:
        """
        print "An error occurred at request " + repr(request) + ": " + repr(error)
