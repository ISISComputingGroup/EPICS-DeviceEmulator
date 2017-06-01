from lewis.adapters.stream import StreamAdapter
from lewis_emulators.utils.command_builder import CmdBuilder


class Tpg26xStreamInterface(StreamAdapter):
    """
    Stream interface for the serial port
    """

    _last_command = None
    ACK = chr(6)

    commands = {
        CmdBuilder("get_pressure").escape("PRX").build(),
        CmdBuilder("handle_enquiry").enq().build()
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        print "An error occurred at request " + repr(request) + ": " + repr(error)

    def handle_enquiry(self):
        """
        Handle an enquiry using the last command sent.
        :return:
        """

        if self._last_command == "PRX":
            return self.get_pressure()
        else:
            print "Last command was unknown: " + repr(self._last_command)

    def get_pressure(self):
        """
        Get the current pressure of the TPG26x

        Returns: a string with pressure and error codes
        """
        if self._last_command is None:
            self._last_command = "PRX"
            return self.ACK
        else:
            self._last_command = None
            return "0,{0},0,{1}".format(self._device.pressure1, self._device.pressure2)

