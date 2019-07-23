from lewis.adapters.stream import StreamInterface, Cmd
from lewis_emulators.utils.command_builder import CmdBuilder


class Wm323StreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_status").escape("1RS").eos().build(),
        CmdBuilder("set_speed").escape("1SP").int().eos().build(),
        CmdBuilder("set_rotation_cw").escape("1RR").eos().build(),
        CmdBuilder("set_rotation_ccw").escape("1RL").eos().build(),
        CmdBuilder("set_running_start").escape("1GO").eos().build(),
        CmdBuilder("set_running_stop").escape("1ST").eos().build(),
    }

    in_terminator = "\r"
    out_terminator = "\r"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    def get_status(self):
        return "{} {} {} {} !".format(self.device.type, self.device.speed, self.device.direction, self.device.running)

    def set_speed(self, speed):
        self.device.speed = speed

    def set_rotation(self, direction):
        self.device.direction = direction

    def set_rotation_cw(self):
        self.device.direction = "CW"

    def set_rotation_ccw(self):
        self.device.direction = "CCW"

    def set_running_start(self):
        self.device.running = 1

    def set_running_stop(self):
        self.device.running = 0
