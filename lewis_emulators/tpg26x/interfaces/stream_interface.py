from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


class Tpg26xStreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """
    _last_command = None
    ACK = chr(6)

    commands = {
        CmdBuilder("acknowledge_pressure").escape("PRX").build(),
        CmdBuilder("acknowledge_units").escape("UNI").build(),
        CmdBuilder("set_units").escape("UNI").arg("{0|1|2}").build(),
        CmdBuilder("handle_enquiry").enq().build()
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        """
        If command is not recognised print and error.

        :param request: requested string
        :param error: problem
        :return:
        """
        print "An error occurred at request " + repr(request) + ": " + repr(error)

    def acknowledge_pressure(self):
        """
        Acknowledge that the request for current pressure was received.

        :return: ASCII acknowledgement character (0x6)
        """
        self._last_command = "PRX"
        return self.ACK

    def acknowledge_units(self):
        """
        Acknowledge that the request for current units was received.

        :return: ASCII acknowledgement character (0x6)
        """
        self._last_command = "UNI"
        return self.ACK

    def handle_enquiry(self):
        """
        Handle an enquiry using the last command sent.

        :return:
        """

        if self._last_command == "PRX":
            return self.get_pressure()
        elif self._last_command == "UNI":
            return self.get_units()
        else:
            print "Last command was unknown: " + repr(self._last_command)

    def get_pressure(self):
        """
        Get the current pressure of the TPG26x.

        Returns: a string with pressure and error codes
        """
        return "{0},{1},{2},{3}".format(self._device.error1, self._device.pressure1,
                                        self._device.error2, self._device.pressure2)

    def get_units(self):
        """
        Get the current units of the TPG26x.

        Returns: a string representing the units
        """
        return self._device.units

    def set_units(self, units):
        """
        Set the units of the TPG26x.

        :param units: the unit flag to change the units to
        """
        if self._last_command is None:
            self._last_command = "UNI"
            return self.ACK

        self._device.units = units
        self._last_command = None
