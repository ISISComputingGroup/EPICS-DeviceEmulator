"""
Stream device for hlx503
"""

from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


@has_log
class HLX503StreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """

    in_terminator = "\n"
    out_terminator = "\n"

    def __init__(self):

        super(HLX503StreamInterface, self).__init__()
        self.commands = {
            CmdBuilder(self.get_temp).escape("@").int().escape("R").int().eos().build(),
            CmdBuilder(self.set_automode).escape("@").int().escape("A").int().eos().build(),
            CmdBuilder(self.get_status).escape("@").int().escape("X").eos().build(),
        }

    @if_connected
    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    @if_connected
    def get_temp(self, isobus_address: int, channel: int):
        temp = self._device.get_temp(isobus_address, channel)
        return f"{isobus_address}{temp}"

    @if_connected
    def get_status(self, isobus_address: int):
        return self._device.get_status(isobus_address)

    @if_connected
    def set_automode(self, isobus_address: int, automode: int):
        self.log.info(f"AUTOMODE {automode}")
        autoheat = automode & 1 != 0
        self._device.set_autoheat(isobus_address, autoheat)
        autoneedle_valve = automode & 2 != 0
        self._device.set_autoneedlevalve(isobus_address, autoneedle_valve)
