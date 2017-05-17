from lewis.adapters.stream import StreamAdapter
from lewis_emulators.utils.command_builder import CmdBuilder


class Amint2lStreamInterface(StreamAdapter):
    """
    Stream interface for the serial port
    """

    commands = {
        CmdBuilder("get_pressure").stx().arg("[A-Fa-f0-9]+").escape("r").build()
    }

    in_terminator = chr(3)
    out_terminator = chr(3)

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        print "An error occurred at request " + repr(request) + ": " + repr(error)

    def get_pressure(self, address):

        """
        Gets the current pressure

        :param address: address of request
        Returns: pressure in correct format if pressure has a value; if None returns None as if it is disconnected

        """
        if address.upper() != self._device.address.upper():
            print "unknown address {0}".format(address)
            return None
        print str(self._device.pressure)
        if self._device.pressure is None:
            return None
        else:
            try:
                return "{stx}{pressure:+8.3f}".format(stx=chr(2), pressure=self._device.pressure)
            except ValueError:
                # pressure contains string probably OR (over range) or UR (under range)
                return "{stx}{pressure:8s}".format(stx=chr(2), pressure=self._device.pressure)
