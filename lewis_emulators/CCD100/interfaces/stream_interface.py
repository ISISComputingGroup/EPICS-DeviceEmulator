from lewis.adapters.stream import StreamAdapter, Cmd
import random

SP_COMM = "spv"
UNITS_COMM = "uiu"
READING_COMM = "r"


class CCD100StreamInterface(StreamAdapter):

    commands = {
        Cmd("get_sp", "^[a-h]" + SP_COMM + "\?$"),
        Cmd("set_sp", "^[a-h]" + SP_COMM + " ([\-0-9.]+)$", argument_mappings=[float]),
        Cmd("get_units", "^[a-h]" + UNITS_COMM + "\?$"),
        Cmd("set_units", "^[a-h]" + UNITS_COMM + " ([a-z]+)$"),
        Cmd("get_reading", "^[a-h]" + READING_COMM + "$"),
    }

    in_terminator = "\r\n"
    out_terminator = "\r\r\n"

    out_echo = "*{}*:{};{}"
    out_response = "!{}!o!"

    def create_response(self, command, params=" ", data=None):
        out = self.out_echo.format(self._device.address, command, params) + self.out_terminator
        if data:
            out += data + self.out_terminator
        out += self.out_response.format(self._device.address)
        return out

    def get_sp(self):
        return self.create_response(SP_COMM + "?", data="SP VALUE: " + str(self._device.setpoint) + " ")

    def set_sp(self, new_sp):
        self._device.setpoint = new_sp
        return self.create_response(SP_COMM)

    def get_units(self):
        return self.create_response(UNITS_COMM + "?", data="INPUT UNITS STR: " + str(self._device.units))

    def set_units(self, new_units):
        self._device.units = new_units
        return self.create_response(UNITS_COMM)

    def get_reading(self):
        rand = random.random() * 10.0
        data_str = "READ: {:0.3f}".format(rand) + ";" + str(self._device.setpoint_mode)
        return self.create_response(READING_COMM + "  ", data=data_str)

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)

