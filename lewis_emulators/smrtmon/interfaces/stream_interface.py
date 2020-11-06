from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


def _split_command_output(command):
    return command.split(",")


class SmrtmonStreamInterface(StreamInterface):
    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_stat").escape("STAT").build(),
        CmdBuilder("get_oplm").escape("OPLM").build(),
        CmdBuilder("get_lims").escape("LIMS").build(),
    }
    in_terminator = "\r"
    # Out terminator is defined in ResponseBuilder instead as we need to add it to two messages.
    out_terminator = "\r"

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    def get_stat(self):
        return "{},{},{},{},{},{},{},{},{},{},{}".format(*self._device.stat)

    def get_oplm(self):
        return "{},{},{},{},{},{},{},{},{}".format(*self._device.oplm)

    def get_lims(self):
        return "{},{},{},{},{},{},{},{},{}".format(*self._device.lims)