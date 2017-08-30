from lewis.adapters.stream import StreamAdapter
from lewis_emulators.utils.command_builder import CmdBuilder


class EurothermStreamInterface(StreamAdapter):
    """
    Stream interface for the serial port
    """

    commands = {
    }

    in_terminator = chr(3)
    out_terminator = chr(3)

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        print "An error occurred at request " + repr(request) + ": " + repr(error)

