from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


class Tpg300StreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """

    _last_command = None
    ACK = chr(6)
    DEVICE_STATUS = 0

    commands = {
        CmdBuilder("acknowledge_pressure").escape("PA1").build(),
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

    def acknowledge_pressure(self):

        self._last_command = "PA1"
        return self.ACK

    def handle_enquiry(self):
        """
        Handle an enquiry using the last command sent.

        :return:
        """

        if self._last_command == "PA1":
            return "{},{}".format(self.DEVICE_STATUS, self._device.pressure_a1)
        elif self._last_command == "PA2":
            return str(self._device.pressure_a2)
        elif self._last_command == "PB1":
            return str(self._device.pressure_b1)
        elif self._last_command == "PB2":
            return str(self._device.pressure_b2)
        else:
            print("Last command was unknown: ", str(self._last_command))
