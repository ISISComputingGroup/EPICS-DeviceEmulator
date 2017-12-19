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
            CmdBuilder(self.set_position).escape("B/").spaces().escape("X").int().spaces().escape("Y").int()
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
        """
        Get position of the motor axes
        Returns: string indicating postion of motors

        """

        x_axis_return = self.device.x_axis.get_label_and_position()
        y_axis_return = self.device.y_axis.get_label_and_position()
        self.log.info("Send position {} {}".format(x_axis_return, y_axis_return))
        return "{ACK}{STX}{0},{1}".format(x_axis_return, y_axis_return, **COMMAND_CHARS)

    def home_axis(self, axis):
        if axis == "X":
            self.device.x_axis.home()
        elif axis == "Y":
            self.device.y_axis.home()
        return "{ACK}"

    def get_status(self):
        """

        Returns: the moving status of the motor, N not at position, P at position, E error

        """
        if self.device.is_moving_error:
            status = "E"
        else:
            is_moving = self.device.x_axis.moving or self.device.y_axis.moving
            if self.device.is_moving is not None:
                is_moving = self.device.is_moving

            if is_moving:
                status = "N"
            else:
                status = "P"
        self.log.info("Send motor status {}".format(status))
        return "{ACK}{STX}{status}".format(status=status, **COMMAND_CHARS)

    def set_position(self, x_position, y_position):
        self.device.x_axis.sp = x_position
        self.device.y_axis.sp = y_position
        return "{ACK}".format(**COMMAND_CHARS)