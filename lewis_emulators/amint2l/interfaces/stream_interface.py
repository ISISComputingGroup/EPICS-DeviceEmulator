import re

from lewis.adapters.stream import StreamAdapter, Cmd

from lewis_emulators.amint2l.constants import ADDRESS_HIGH, ADDRESS_LOW
from lewis_emulators.utils.command_builder import CmdBuilder


class Amint2lStreamInterface(StreamAdapter):
    """
    Stream interface for the serial port
    """

    commands = {
        CmdBuilder("get_pressure").stx().
            escape("{address_high}{address_low}r".format(address_high=ADDRESS_HIGH, address_low=ADDRESS_LOW)).build()
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

    def get_pressure(self):

        """
        Gets the current pressure

        Returns: pressure in correct format if pressure has a value; if None returns None as if it is disconnected

        """

        if self._device.pressure is None:
            return None
        else:
            try:
                return "{stx}{pressure:+8.3f}".format(stx=chr(2), pressure=self._device.pressure)
            except ValueError:
                # pressure contains string probably OR (over range) or UR (under range)
                return "{stx}{pressure:8s}".format(stx=chr(2), pressure=self._device.pressure)
