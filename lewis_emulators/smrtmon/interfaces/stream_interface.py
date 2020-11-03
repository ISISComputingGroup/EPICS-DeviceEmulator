from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


class SmrtmonStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_stat1").escape("STAT").build(),
        CmdBuilder("get_oplm1").escape("OPLM").build(),
        CmdBuilder("get_lims1").escape("LIMS").build(),
    }

    in_terminator = "\r"

    # Out terminator is defined in ResponseBuilder instead as we need to add it to two messages.
    out_terminator = "\r"

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    def get_stat1(self):
        return self._device.get_stat1()

    def get_oplm1(self):
        return self.device.get_oplm1()

    def get_lims1(self):
        return self.device.get_lims1()
