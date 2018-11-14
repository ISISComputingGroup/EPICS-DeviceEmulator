from lewis.adapters.stream import StreamInterface

from lewis.core.logging import has_log
from lewis_emulators.utils.replies import conditional_reply
from lewis_emulators.utils.command_builder import CmdBuilder

if_connected = conditional_reply('connected')

@has_log
class Knr1050StreamInterface(StreamInterface):

    in_terminator = '\r'
    out_terminator = '\r'

    def __init__(self):

        super(Knr1050StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.stop).escape('STOP:1,0').build()
        }


    def handle_error(self, request, error):
        """
        If command is not recognised print and error
        Args:
            request: requested string
            error: problem
        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def stop(self):
        self.device.is_stopped = True
