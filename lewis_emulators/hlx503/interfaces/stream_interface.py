"""
Stream device for hlx503
"""

from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


@has_log
class HLX503StreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """

    in_terminator = chr(3)
    out_terminator = chr(3)

    def __init__(self):

        super(HLX503StreamInterface, self).__init__()
        self.commands = {}

    @if_connected
    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))
