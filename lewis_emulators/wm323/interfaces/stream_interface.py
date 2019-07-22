from lewis.adapters.stream import StreamInterface, Cmd
from lewis_emulators.utils.command_builder import CmdBuilder


class Wm323StreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_status").escape("1RS").eos().build(),
        CmdBuilder("set_speed").escape("1SP").int().eos().build(),
    }

    in_terminator = "\r"
    out_terminator = "\r"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    def get_status(self):
        return "323Du {} CW 1 !".format(self.device.speed)

    def set_speed(self, speed):
        self.device.speed = speed
