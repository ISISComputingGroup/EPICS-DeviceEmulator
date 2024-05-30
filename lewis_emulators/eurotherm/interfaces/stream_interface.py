from lewis.adapters.stream import StreamInterface
from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply

if_connected = conditional_reply("connected")

#TODO: add address params to methods 
class EurothermStreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """

    commands = {
        CmdBuilder("get_current_temperature").eot().int().regex("PV").enq().build(),
        CmdBuilder("get_setpoint").eot().int().regex("SL").enq().build(),
        CmdBuilder("get_ramp_setpoint").eot().int().regex("SP").enq().build(),
        CmdBuilder("get_output").eot().int().regex("OP").enq().build(),
        CmdBuilder("get_max_output").eot().int().regex("HO").enq().build(),
        CmdBuilder("get_output_rate").eot().int().regex("OR").enq().build(),
        CmdBuilder("get_autotune").eot().int().regex("AT").enq().build(),
        CmdBuilder("get_proportional").eot().int().regex("XP").enq().build(),
        CmdBuilder("get_derivative").eot().int().regex("TD").enq().build(),
        CmdBuilder("get_integral").eot().int().regex("TI").enq().build(),
        CmdBuilder("get_highlim").eot().int().regex("HS").enq().build(),
        CmdBuilder("get_lowlim").eot().int().regex("LS").enq().build(),
        CmdBuilder("get_error").eot().int().regex("EE").enq().build(),
        CmdBuilder("get_address").eot().int().regex("").enq().build(),

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
    def get_address(self):
        """
        Get the address of the specific Eurotherm sensor, i.e. A01 or 0011
        """
        return self.make_read_reply(self._device.address())
    
    @if_connected
    def get_setpoint(self, addr):
        try:
            return self.make_read_reply("SL", self._device.setpoint_temperature(addr))
        except:
            return None

    @if_connected
    def get_proportional(self, addr):
        try:
            return self.make_read_reply("XP", self.device.p(addr))
        except:
            return None

    @if_connected
    def get_integral(self, addr):
        try:
            return self.make_read_reply("TI", self.device.i(addr))
        except:
            return None

    @if_connected
    def get_derivative(self, addr):
        try:
            return self.make_read_reply("TD", self.device.d(addr))
        except: 
            return None
        
    @if_connected
    def get_output(self, addr):
        try:
            return self.make_read_reply("OP", self.device.output(addr))
        except:
            return None

    @if_connected
    def get_highlim(self):
        try:
            return self.make_read_reply("HS", self.device.high_lim)
        except:
            return None

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
        self.device.set_output_rate = output_rate
        return "\x06"

    @if_connected
    def get_autotune(self):
        return self.make_read_reply("AT", self.device.autotune)

    @if_connected
    def get_current_temperature(self, addr):
        """
        Get the current temperature of the device.

        Returns: the current temperature formatted like the Eurotherm protocol.
        """
        try:
            return self.make_read_reply("PV", self._device.current_temperature(addr))
        except:
            return None

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
        self._device.set_ramp_setpoint_temperature = temperature
        return "\x06"

    @if_connected
    def get_error(self):
        """
        Get the error.

        Returns: the current error code in HEX.
        """
        reply = "\x02EE>0x{}\x03".format(self._device.error)
        return f"{reply}{self.make_checksum(reply[1:])}"
