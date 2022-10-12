from lewis.adapters.stream import StreamInterface
from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


class EurothermStreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """

    commands = {
        CmdBuilder("get_current_temperature").eot().escape("0011PV").enq().build(),
        CmdBuilder("get_ramp_setpoint").eot().escape("0011SP").enq().build(),
        CmdBuilder("get_output").eot().escape("0011OP").enq().build(),
        CmdBuilder("get_max_output").eot().escape("0011HO").enq().build(),
        CmdBuilder("get_autotune").eot().escape("0011AT").enq().build(),
        CmdBuilder("get_proportional").eot().escape("0011XP").enq().build(),
        CmdBuilder("get_derivative").eot().escape("0011TD").enq().build(),
        CmdBuilder("get_integral").eot().escape("0011TI").enq().build(),
        CmdBuilder("get_highlim").eot().escape("0011HS").enq().build(),
        CmdBuilder("get_lowlim").eot().escape("0011LS").enq().build(),

        CmdBuilder("set_ramp_setpoint", arg_sep="").eot().escape("0011").stx().escape("SL").float().etx().any().build(),
    }

    in_terminator = ""
    out_terminator = "\x03"
    readtimeout = 1

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    @if_connected
    def get_proportional(self):
        return "\x02XP{}".format(self.device.p)

    @if_connected
    def get_integral(self):
        return "\x02TI{}".format(self.device.i)

    @if_connected
    def get_derivative(self):
        return "\x02TD{}".format(self.device.d)

    @if_connected
    def get_output(self):
        return "\x02OP{}".format(self.device.output)

    @if_connected
    def get_highlim(self):
        return "\x02HS{}".format(self.device.high_lim)

    @if_connected
    def get_lowlim(self):
        return "\x02LS{}".format(self.device.low_lim)

    @if_connected
    def get_max_output(self):
        return "\x02HO{}".format(self.device.max_output)

    @if_connected
    def get_autotune(self):
        return "\x02AT{}".format(self.device.autotune)

    @if_connected
    def get_current_temperature(self):
        """
        Get the current temperature of the device.

        Returns: the current temperature formatted like the Eurotherm protocol.
        """
        return "\x02PV{}".format(self._device.current_temperature)

    @if_connected
    def get_ramp_setpoint(self):
        """
        Get the set point temperature.

        Returns: the current set point temperature formatted like the Eurotherm protocol.
        """
        return "\x02SP{}".format(self._device.ramp_setpoint_temperature)

    @if_connected
    def set_ramp_setpoint(self, temperature, _):
        """
        Set the set point temperature.

        Args:
            temperature: the temperature to set the setpoint to.
            _: unused argument captured by the command.

        """
        self._device.ramp_setpoint_temperature = temperature
