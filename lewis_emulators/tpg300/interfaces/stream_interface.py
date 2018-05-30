from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder


class Tpg300StreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """

    _last_command = None
    ACK = chr(6)
    DEVICE_STATUS = 0

    commands = {
        CmdBuilder("acknowledge_pressure").escape("P").arg("A1|A2|B1|B2").build(),
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
        print("An error occurred at request ", str(request), ": ", str(error))

    def acknowledge_pressure(self, request):

        self._last_command = "P{}".format(request)
        print(self._last_command)
        return self.ACK

    def define_channel_lookup(self):
        """
        Defines a lookup dictionary for the 4 pressure channels

        Returns:
            A dictionary which points to the 4 pressure variables
        """

        return {"PA1": self._device.pressure_a1,
                "PA2": self._device.pressure_a2,
                "PB1": self._device.pressure_b1,
                "PB2": self._device.pressure_b2}

    @has_log
    def handle_enquiry(self):
        """
        Handle an enquiry using the last command sent.

        :return:
        """

        channel_lookup = self.define_channel_lookup()

        if self._last_command in channel_lookup:
            return "{},{}".format(self.DEVICE_STATUS, channel_lookup[self._last_command])
        elif self._last_command == "UNI":
            return "{},{}".format("")
        else:
            print("Last command was unknown: ", str(self._last_command))
