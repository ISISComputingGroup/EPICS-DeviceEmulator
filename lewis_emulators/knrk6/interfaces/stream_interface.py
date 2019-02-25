from lewis.adapters.stream import StreamInterface, Cmd

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply('connected')


class Knrk6StreamInterface(StreamInterface):

    in_terminator = '\r'
    out_terminator = '\r'

    # Commands that we expect via serial during normal operation
    def __init__(self):

        super(Knrk6StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.get_position).escape("p").eos().build(),
            CmdBuilder(self.set_position).int().eos().build(),
            CmdBuilder(self.get_valve_type).escape("t").eos().build(),
        }

    def catch_all(self):
        pass

    @if_connected
    def get_position(self):
        return self.device.position

    @if_connected
    def set_position(self, position):
        self.device.position = position
        return "OK"

    @if_connected
    def get_valve_type(self):
        return self.device.valve_type
