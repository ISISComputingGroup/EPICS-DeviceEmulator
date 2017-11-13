from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder

@has_log
class FZJDDFCHStreamInterface(StreamInterface):
    """
    Stream interface for the Ethernet port
    """

    commands = {
        CmdBuilder("get_magnetic_bearing_state").escape("MBON?").build()
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
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def get_magnetic_bearing_state(self):

        """
        Gets the 

        :param address: address of request
        Returns: pressure in correct format if pressure has a value; if None returns None as if it is disconnected

        """
        return self._device.magnetic_bearing_state
