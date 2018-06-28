from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply


class RkndioStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_idn").escape("*IDN?").eos().build(),
        CmdBuilder("get_status").escape("STATUS").eos().build(),
        CmdBuilder("get_error").escape("ERR").eos().build()
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        """
        Prints an error message if a command is not recognised.

        Args:
            request : Request.
            error: The error that has occurred.
        Returns:
            None.
        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

        print("An error occurred at request {}: {}".format(request, error))

    @conditional_reply("connected")
    def get_idn(self):
        return self._device.idn

    @conditional_reply("connected")
    def get_status(self):
        return self._device.status

    @conditional_reply("connected")
    def get_error(self):
        return self._device.error


