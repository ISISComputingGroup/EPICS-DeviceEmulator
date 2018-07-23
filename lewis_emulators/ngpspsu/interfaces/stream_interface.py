from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


class NgpspsuStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_version").escape("VER").build()
    }

    out_terminator = "\r"
    in_terminator = "\r\n"

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

    def get_version(self):
        """

        Returns:
            The device's model number and firmware.
        """
        return "#VER:{}".format(self._device.model_number_and_firmware)

