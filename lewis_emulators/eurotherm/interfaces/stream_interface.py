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
        CmdBuilder("get_current_temperature").eot().int().escape("PV").enq().build(),
        CmdBuilder("get_setpoint").eot().int().escape("SL").enq().build(),
        CmdBuilder("get_ramp_setpoint").eot().int().escape("SP").enq().build(),
        CmdBuilder("get_output").eot().int().escape("OP").enq().build(),
        CmdBuilder("get_max_output").eot().int().escape("HO").enq().build(),
        CmdBuilder("get_output_rate").eot().int().escape("OR").enq().build(),
        CmdBuilder("get_autotune").eot().int().escape("AT").enq().build(),
        CmdBuilder("get_proportional").eot().int().escape("XP").enq().build(),
        CmdBuilder("get_derivative").eot().int().escape("TD").enq().build(),
        CmdBuilder("get_integral").eot().int().escape("TI").enq().build(),
        CmdBuilder("get_highlim").eot().int().escape("HS").enq().build(),
        CmdBuilder("get_lowlim").eot().int().escape("LS").enq().build(),
        CmdBuilder("get_error").eot().int().escape("EE").enq().build(),
        CmdBuilder("get_address").eot().int().escape("").enq().build(),

        CmdBuilder("set_ramp_setpoint", arg_sep="").eot().int().stx().escape("SL").float().etx().any().build(),
        CmdBuilder("set_output_rate", arg_sep="").eot().int().stx().escape("OR").float().etx().any().build(),
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
        reply = f"\x02{command}{str(value)}\x03"
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
    def get_address(self, addr):
        """
        Get the address of the specific Eurotherm sensor, i.e. A01 or 0011
        """
        return self.make_read_reply(self.device.address(addr))
    
    @if_connected
    def get_setpoint(self, addr):
        try:
            return self.make_read_reply("SL", self.device.setpoint_temperature(addr))
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
    def get_highlim(self, addr):
        try:
            return self.make_read_reply("HS", self.device.high_lim(addr))
        except:
            return None

    @if_connected
    def get_lowlim(self, addr):
        try:
            return self.make_read_reply("LS", self.device.low_lim(addr))
        except:
            return None

    @if_connected
    def get_max_output(self, addr):
        try:
            return self.make_read_reply("HO", self.device.max_output(addr))
        except:
            return None
        
    @if_connected
    def get_autotune(self, addr):
        try:
            return self.make_read_reply("AT", self.device.autotune(addr))
        except:
            return None

    @if_connected
    def get_current_temperature(self, addr):
        """
        Get the current temperature of the device.

        Returns: the current temperature formatted like the Eurotherm protocol.
        """
        try:
            return self.make_read_reply("PV", self.device.current_temperature(addr))
        except:
            return None

    @if_connected
    def get_output_rate(self, addr):
        try:
            return self.make_read_reply("OR", self.device.output_rate(addr))
        except:
            return None

    @if_connected
    def set_output_rate(self, addr, output_rate, _):
        try:
            self.device.set_output_rate(addr, output_rate)
            return "\x06"
        except:
            return None

    @if_connected
    def get_ramp_setpoint(self, addr):
        """
        Get the set point temperature.

        Returns: the current set point temperature formatted like the Eurotherm protocol.
        """
        try:
            return self.make_read_reply("SP", self.device.ramp_setpoint_temperature(addr))
        except: 
            return None

    @if_connected
    def set_ramp_setpoint(self, addr, temperature, _):
        """
        Set the set point temperature.

        Args:
            temperature: the temperature to set the setpoint to.
            _: argument captured by the command.

        """
        try:
            self.device.set_ramp_setpoint_temperature(addr, temperature)
            return "\x06"
        except:
            return None

    @if_connected
    def get_error(self, addr):
        """
        Get the error.

        Returns: the current error code in HEX.
        """
        reply = "\x02EE>0x{}\x03".format(self.device.error(addr))
        return f"{reply}{self.make_checksum(reply[1:])}"
