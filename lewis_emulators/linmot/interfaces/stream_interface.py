from lewis.adapters.stream import StreamInterface, Cmd

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


class LinmotStreamInterface(StreamInterface):

    in_terminator = "\r\n"
    out_terminator = "\r"

    readtimeout = 5000

    def __init__(self):

        super(LinmotStreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self. commands = {
            CmdBuilder(self.set_position).escape("!SP").int().escape("A").eos().build(),
            CmdBuilder(self.get_position).escape("!GPA").eos().build(),
            CmdBuilder(self.get_actual_speed_resolution).escape("!VIA").eos().build(),
            CmdBuilder(self.get_motor_warn_status).escape("!EWA").eos().build(),
            CmdBuilder(self.get_motor_error_status).escape("!EEA").eos().build(),
            CmdBuilder(self.set_maximal_speed).escape("!SV").int().escape("A").eos().build(),
            CmdBuilder(self.set_maximal_acceleration).escape("!SA").int().escape("A").eos().build(),
            }

    @if_connected
    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    @if_connected
    def set_position(self, target_position):
        self.device.target_position = target_position
        self.device.new_action = True
        self.device.position_reached = False
        return "#"

    @if_connected
    def get_position(self):
        return "#{position}".format(position=self.device.position)

    @if_connected
    def get_actual_speed_resolution(self):
        return "#{speed_resolution}".format(speed_resolution=self.device.speed_resolution)

    @if_connected
    def get_motor_warn_status(self):
        return "#{motor_warn_status}".format(motor_warn_status=self.device.motor_warn_status)

    @if_connected
    def get_motor_error_status(self):
        return "#{motor_error_status}".format(motor_error_status=self.device.motor_error_status)

    @if_connected
    def set_maximal_speed(self, speed):
        self.device.maximal_speed = int(speed)
        return "#"

    @if_connected
    def set_maximal_acceleration(self, acceleration):
        self.device.maximal_acceleration = int(acceleration)
        return "#"

    @if_connected
    def catch_all(self):
        pass
