from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


@has_log
class MezfliprStreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """

    in_terminator = ""
    out_terminator = ":"

    commands = {
        CmdBuilder("get_idn").escape("*IDN?").eos().build(),
    }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    @if_connected
    def get_idn(self):

        """
        Gets the current pressure

        :param address: address of request
        Returns: pressure in correct format if pressure has a value; if None returns None as if it is disconnected

        """
        return "Simulated mezei flipper"
