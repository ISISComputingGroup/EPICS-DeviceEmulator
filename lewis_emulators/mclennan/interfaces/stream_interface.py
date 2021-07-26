from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


@has_log
class MclennanStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("stop").int().escape("ST").eos().build(),
        CmdBuilder("identify").int().escape("ID").eos().build(),
        CmdBuilder("status").int().escape("OS").eos().build(),
        CmdBuilder("get_position").int().escape("OA").eos().build(),
        CmdBuilder("set_accel").int().escape("SA").int().eos().build(),
        CmdBuilder("set_decel").int().escape("SD").int().eos().build(),
        CmdBuilder("set_creep_speed").int().escape("SC").int().eos().build(),
        CmdBuilder("reset").int().escape("RS").eos().build(),
        CmdBuilder("jog").int().escape("CV").int().eos().build(),
        CmdBuilder("query_speeds").int().escape("QS").eos().build(),
    }

    in_terminator = "\r"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    @if_connected
    def stop(self, controller):
        self.device.stop()
        return "OK"

    @if_connected
    def identify(self, controller):
        return "01: PM600 Ver 3.02" if not self.device.is_pm304 else "1:Mclennan Servo Supplies Ltd. PM304 V6.15"

    @if_connected
    def query_speeds(self, controller):
        return f"SV=16200,SC={self.device.creep_speed},SA=100000,SD=100000" if self.device.is_pm304 else f"01:SC = {self.device.creep_speed} SV = 16200 SA = 100000 SD = 100000 LD = 200000"

    @if_connected
    def set_creep_speed(self, controller, creep_speed):
        self.device.creep_speed = creep_speed
        return "OK"

    @if_connected
    def status(self, controller):
        return f"01:{int(not self.device.is_jogging)}000{int(self.device.is_jogging)}000"

    @if_connected
    def get_position(self, controller):
        return f"01:{int(self.device.position)}"

    @if_connected
    def set_accel(self, controller, acceleration):
        return "OK"

    @if_connected
    def set_decel(self, controller, deceleration):
        return "OK"

    @if_connected
    def reset(self, controller):
        return "RESET"

    @if_connected
    def jog(self, controller, velocity):
        self.device.jog(velocity)
        return "OK"
    
