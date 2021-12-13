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

    # The real Eurotherm uses timeouts instead of terminators to assess when a command is finished. To make this work
    # with the emulator we manually added terminators via asyn commands to the device. Lewis will be able to handle this
    # natively in future versions. See: https://github.com/DMSC-Instrument-Data/lewis/pull/262
    in_terminator = "\r\n"
    out_terminator = chr(3)

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
        """
        TODO: Get the proportional of the device's PID values
        """
        return "\x02XP0"

    @if_connected
    def get_integral(self):
        """
        TODO: Get the integral of the device's PID values
        """
        return "\x02TI0"

    @if_connected
    def get_derivative(self):
        """
        TODO: Get the derivative of the device's PID values
        """
        return "\x02TD0"

    @if_connected
    def get_output(self):
        """
        TODO: Get the output of the device
        """
        return "\x02OP0"

    @if_connected
    def get_highlim(self):
        """
        TODO: Get the high limit of the device
        """
        return "\x02HS0"

    @if_connected
    def get_lowlim(self):
        """
        TODO: Get the low limit of the device
        """
        return "\x02LS0"

    @if_connected
    def get_max_output(self):
        """
        TODO: Get the max output of the device
        """
        return "\x02HO0"

    @if_connected
    def get_autotune(self):
        """
        TODO: Get the max output of the device
        """
        return "\x02AT0"

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
