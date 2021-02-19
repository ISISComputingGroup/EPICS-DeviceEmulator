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
            CmdBuilder(self.set_temp).escape("@").int().escape("T").float().eos().build(),
            CmdBuilder(self.set_automode).escape("@").int().escape("A").int().eos().build(),
            CmdBuilder(self.set_ctrlchannel).escape("@").int().escape("H").int().eos().build(),
            CmdBuilder(self.set_autopid).escape("@").int().escape("L").int().eos().build(),
            CmdBuilder(self.set_ctrl_mode).escape("@").int().escape("C").int().eos().build(),
            CmdBuilder(self.set_proportional).escape("@").int().escape("P").float().eos().build(),
            CmdBuilder(self.set_integral).escape("@").int().escape("I").float().eos().build(),
            CmdBuilder(self.set_derivative).escape("@").int().escape("D").float().eos().build(),
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
        return f"@{isobus_address}R{temp}"

    @if_connected
    def set_temp(self, isobus_address: int, temp: float):
        self.log.info(f"SET TEMP {temp}")
        self._device.set_temp(isobus_address, temp)

    @if_connected
    def get_status(self, isobus_address: int):
        return self._device.get_status(isobus_address)

    @if_connected
    def set_automode(self, isobus_address: int, automode: int):
        autoheat = automode & 1 != 0
        self._device.set_autoheat(isobus_address, autoheat)
        autoneedle_valve = automode & 2 != 0
        self._device.set_autoneedlevalve(isobus_address, autoneedle_valve)

    @if_connected
    def set_autopid(self, isobus_address: int, autopid: int):
        self._device.set_autopid(isobus_address, bool(autopid))

    @if_connected
    def set_ctrl_mode(self, isobus_address: int, ctrl_mode: int):
        remote = ctrl_mode & 1 != 0
        self._device.set_remote(isobus_address, remote)
        locked = ctrl_mode & 2 != 0
        self._device.set_locked(isobus_address, locked)

    @if_connected
    def set_ctrlchannel(self, isobus_address: int, ctrlchannel: int):
        self._device.set_ctrlchannel(isobus_address, ctrlchannel)

    @if_connected
    def set_proportional(self, isobus_address: int, proportional: float):
        self._device.set_proportional(isobus_address, proportional)

    @if_connected
    def set_integral(self, isobus_address: int, integral: float):
        self._device.set_integral(isobus_address, integral)

    @if_connected
    def set_derivative(self, isobus_address: int, derivative: float):
        self._device.set_derivative(isobus_address, derivative)
