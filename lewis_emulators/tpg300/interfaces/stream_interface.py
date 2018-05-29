from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


class Tpg300StreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """

    _last_command = None
    ACK = chr(6)

    commands = {
        CmdBuilder("acknowledge_pressure").escape("P").arg("{A1|A2|B1|B2}").build(),
        CmdBuilder("handle_enquiry").enq().build()
    }

    def acknowledge_pressure(self, channel):

        self._last_command = "P"+channel
        return self.ACK

    def handle_enquiry(self):
        """
        Handle an enquiry using the last command sent.

        :return:
        """

        if self._last_command == "PA1":
            return str(self._device.pressure_A1)
        elif self._last_command == "PA2":
            return str(self._device.pressure_A2)
        elif self._last_command == "PB1":
            return str(self._device.pressure_B1)
        elif self._last_command == "PB2":
            return str(self._device.pressure_B2)
        else:
            print "Last command was unknown: " + repr(self._last_command)
