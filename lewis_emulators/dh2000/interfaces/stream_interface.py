from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log


@has_log
class Dh2000StreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_status").escape("&STS!").eos().build(),
        CmdBuilder("close_shutter").escape("&CLOSEA!").eos().build(),
        CmdBuilder("open_shutter").escape("&OPENA!").eos().build(),
        CmdBuilder("invalid_command").eos().build(),
    }

    in_terminator = "\r"
    out_terminator = "\r"

    ACK = "&ACK!" + out_terminator

    @staticmethod
    def handle_error(request, error):
        """
        Prints an error message if a command is not recognised.

        Args:
            request : Request.
            error: The error that has occurred.
        Returns:
            None.
        """

        print("An error occurred at request {}: {}".format(request, error))

    def invalid_command(self):
        if self._device.is_disconnected:
            return None
        else:
            return "&NAC!{}&TYPERR!".format(self.out_terminator)

    def close_shutter(self):
        self._device.shutter_is_open = False

        if self._device.is_disconnected:
            return None
        else:
            return self.ACK

    def open_shutter(self):
        self._device.shutter_is_open = True

        if self._device.is_disconnected:
            return None
        else:
            return self.ACK

    def get_status(self):
        shutter = self._device.shutter_is_open
        interlock = self._device.interlock_is_triggered

        status_string = "{ACK}&A{shutter},I{intlock}!".format(ACK=self.ACK, shutter=int(shutter), intlock=int(interlock))

        if self._device.is_disconnected:
            return None
        else:
            return status_string

    def catch_all(self):
        pass
