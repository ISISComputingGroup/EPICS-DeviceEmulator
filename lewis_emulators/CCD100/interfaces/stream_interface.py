from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply

if_connected = conditional_reply("connected")

SP_COMM = "spv"
UNITS_COMM = "uiu"
READING_COMM = "r"


@has_log
class CCD100StreamInterface(StreamInterface):

    commands = {
        CmdBuilder("get_sp").char(ignore=True).escape(SP_COMM + "?").eos().build(),
        CmdBuilder("set_sp").char().escape(SP_COMM + " ").float().eos().build(),
        CmdBuilder("get_units").char(ignore=True).escape(UNITS_COMM + "?").eos().build(),
        CmdBuilder("set_sp").char().escape(UNITS_COMM + " ").string().eos().build(),
        CmdBuilder("get_reading").char(ignore=True).escape(READING_COMM).eos().build(),
    }

    in_terminator = "\r\n"
    good_out_terminator = "\r\r\n"

    out_echo = "*{}*:{};{}"
    out_response = "!{}!o!"

    def create_response(self, command, params=" ", data=None):
        if self._device.is_giving_errors:
            self.out_terminator = self._device.out_terminator_in_error
            return self._device.out_error
        else:
            self.out_terminator = self.good_out_terminator
            out = self.out_echo.format(self._device.address, command, params) + self.out_terminator
            if data:
                out += data + self.out_terminator
            out += self.out_response.format(self._device.address)
            return out

    @if_connected
    def get_sp(self):
        return self.create_response(SP_COMM + "?", data="SP VALUE: " + str(self._device.setpoint) + " ")

    @if_connected
    def set_sp(self, addr, new_sp):
        if self._device.address == addr:
            self._device.setpoint = new_sp
        return self.create_response(SP_COMM)

    @if_connected
    def get_units(self):
        return self.create_response(UNITS_COMM + "?", data="INPUT UNITS STR: " + str(self._device.units))

    @if_connected
    def set_units(self, addr, new_units):
        if self._device.address == addr:
            self._device.units = new_units
        return self.create_response(UNITS_COMM)

    @if_connected
    def get_reading(self):
        min_width = 10
        data_str = "READ:" + "{:0.3f}".format(self._device.current_reading).ljust(min_width) + ";" + str(self._device.setpoint_mode)
        return self.create_response(READING_COMM + "  ", data=data_str)

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))

