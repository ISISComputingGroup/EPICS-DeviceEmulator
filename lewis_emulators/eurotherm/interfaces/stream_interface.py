from lewis.adapters.stream import StreamInterface
from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


class EurothermStreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """

    commands = {
        CmdBuilder("get_current_temperature").eot().regex("[0-9]{4}PV").enq().build(),
        CmdBuilder("get_setpoint").eot().regex("[0-9]{4}SL").enq().build(),
        CmdBuilder("get_ramp_setpoint").eot().regex("[0-9]{4}SP").enq().build(),
        CmdBuilder("get_output").eot().regex("[0-9]{4}OP").enq().build(),
        CmdBuilder("get_max_output").eot().regex("[0-9]{4}HO").enq().build(),
        CmdBuilder("get_output_rate").eot().regex("[0-9]{4}OR").enq().build(),
        CmdBuilder("get_autotune").eot().regex("[0-9]{4}AT").enq().build(),
        CmdBuilder("get_proportional").eot().regex("[0-9]{4}XP").enq().build(),
        CmdBuilder("get_derivative").eot().regex("[0-9]{4}TD").enq().build(),
        CmdBuilder("get_integral").eot().regex("[0-9]{4}TI").enq().build(),
        CmdBuilder("get_highlim").eot().regex("[0-9]{4}HS").enq().build(),
        CmdBuilder("get_lowlim").eot().regex("[0-9]{4}LS").enq().build(),
        CmdBuilder("get_error").eot().regex("[0-9]{4}EE").enq().build(),

        CmdBuilder("set_ramp_setpoint", arg_sep="").eot().regex("[0-9]{4}").stx().escape("SL").float().etx().any().build(),
        CmdBuilder("set_output_rate", arg_sep="").eot().regex("[0-9]{4}").stx().escape("OR").float().etx().any().build(),
    }

    # Add terminating characters manually for each command, as write and read commands use different formatting for their 'in' commands.
    in_terminator = ""
    out_terminator = ""
    readtimeout = 1

    # calculate a eurotherm xor checksum character from a data string    
    def make_checksum(self, chars):
        checksum = 0
        for c in chars:
            checksum ^= ord(c)
        return chr(checksum)
    
    def make_read_reply(self, command, value):
        reply = f"\x02{command}{value}\x03"
        # checksum calculated on characters after \x02 but up to and including \x03 
        return f"{reply}{self.make_checksum(reply[1:])}"

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    @if_connected
    def get_setpoint(self):
        return self.make_read_reply("SL", self.device._setpoint_temperature)

    @if_connected
    def get_proportional(self):
        return self.make_read_reply("XP", self.device.p)

    @if_connected
    def get_integral(self):
        return self.make_read_reply("TI", self.device.i)

    @if_connected
    def get_derivative(self):
        return self.make_read_reply("TD", self.device.d)

    @if_connected
    def get_output(self):
        return self.make_read_reply("OP", self.device.output)

    @if_connected
    def get_highlim(self):
        return self.make_read_reply("HS", self.device.high_lim)

    @if_connected
    def get_lowlim(self):
        return self.make_read_reply("LS", self.device.low_lim)

    @if_connected
    def get_max_output(self):
        return self.make_read_reply("HO", self.device.max_output)

    @if_connected
    def get_output_rate(self):
        return self.make_read_reply("OR", self.device.output_rate)

    @if_connected
    def set_output_rate(self, output_rate, _):
        self.device.output_rate = output_rate
        return "\x06"

    @if_connected
    def get_autotune(self):
        return self.make_read_reply("AT", self.device.autotune)

    @if_connected
    def get_current_temperature(self):
        """
        Get the current temperature of the device.

        Returns: the current temperature formatted like the Eurotherm protocol.
        """
        return self.make_read_reply("PV", self._device.current_temperature)

    @if_connected
    def get_ramp_setpoint(self):
        """
        Get the set point temperature.

        Returns: the current set point temperature formatted like the Eurotherm protocol.
        """
        return self.make_read_reply("SP", self._device.ramp_setpoint_temperature)

    @if_connected
    def set_ramp_setpoint(self, temperature, _):
        """
        Set the set point temperature.

        Args:
            temperature: the temperature to set the setpoint to.
            _: argument captured by the command.

        """
        self._device.ramp_setpoint_temperature = temperature
        return "\x06"

    @if_connected
    def get_error(self):
        """
        Get the error.

        Returns: the current error code in HEX.
        """
        reply = "\x02EE>0x{}\x03".format(self._device.error)
        return f"{reply}{self.make_checksum(reply[1:])}"
