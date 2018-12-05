from lewis.adapters.stream import StreamInterface, Cmd
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log


@has_log
class Dh2000StreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_status").escape("&STS!").eos().build(),
    }

    in_terminator = "\r"
    out_terminator = "\r"

    ACK = "&ACK!" + out_terminator

    def get_status(self):
        shutter = self._device.shutter_is_open
        interlock = self._device.interlock_is_triggered

        status_string = "{ACK}&A{shutter},I{intlock}!".format(ACK=self.ACK, shutter=int(shutter), intlock=int(interlock))
        self.log.info(status_string)

        return status_string

    def catch_all(self):
        pass
