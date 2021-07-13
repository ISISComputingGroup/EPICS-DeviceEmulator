from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log

from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


@has_log
class WbvalveStreamInterface(StreamInterface):

    in_terminator = '\r\n'
    out_terminator = '\r\n'

    def __init__(self):

        super(WbvalveStreamInterface, self).__init__()
        self.commands = {
            CmdBuilder(self.get_position).escape("st").eos().build(),
            CmdBuilder(self.set_position).escape("wb").int().escape("on").eos().build()
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
    def get_position(self):
        """
        Returns: the position of the water bath valve
        """
        return "wb{}on".format(self.device.wb_position)

    @if_connected
    def set_position(self, valve_position):
        """
        Args:
            valve_position (str): requested valve position
        """
        self.device.wb_position = int(valve_position)
