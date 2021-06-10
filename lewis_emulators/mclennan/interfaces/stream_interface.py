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
        CmdBuilder("reset").int().escape("RS").eos().build(),
        CmdBuilder("jog").int().escape("CV").int().eos().build(),
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
        return "01: PM600 Ver 3.02"

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
    
