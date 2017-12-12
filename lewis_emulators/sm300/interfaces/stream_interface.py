from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.constants import ACK, STX, EOT, COMMAND_CHARS


@has_log
class Sm300StreamInterface(StreamInterface):

    in_terminator = EOT
    out_terminator = EOT

    def __init__(self):

        super(Sm300StreamInterface, self).__init__()

        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.get_position).escape("LQ").build(),  # Catch-all command for debugging
            CmdBuilder(self.home_axis).escape("BR").char().build(),  # Catch-all command for debugging
            CmdBuilder(self.get_status).escape("LM").build(),  # Catch-all command for debugging
        }

        self.device = self._device

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def get_position(self):
        self.device.x_axis.rbv += 0.1
        self.device.x_axis.sp += 0.1
        self.log.info("Send position {} {}".format(self.device.x_axis.rbv, self.device.y_axis.rbv))
        return "{ACK}{STX}X{0:.0f},Y{1:.0f}".format(self.device.x_axis.rbv, self.device.y_axis.rbv, **COMMAND_CHARS)

    def home_axis(self, axis):
        if axis == "X":
            self.device.x_axis.home()
        elif axis == "Y":
            self.device.y_axis.home()
        return "{ACK}"

    def get_status(self):
        if self.device.x_axis.moving or self.device.y_axis.moving:
            status = "N"
        else:
            status = "P"
        return "{ACK}{STX}{status}".format(status=status, **COMMAND_CHARS)
