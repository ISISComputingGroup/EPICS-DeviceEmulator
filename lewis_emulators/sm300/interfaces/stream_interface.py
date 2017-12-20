"""
Stream interface for the SM 300 motor emulator
"""
from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.constants import EOT, COMMAND_CHARS


@has_log
class Sm300StreamInterface(StreamInterface):
    """
    Stream interface for the SM 300 motor emulator
    """
    in_terminator = EOT
    out_terminator = ""

    def __init__(self):

        super(Sm300StreamInterface, self).__init__()

        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.get_position).escape("LQ").build(),
            CmdBuilder(self.get_position_as_steps).escape("LI").char().build(),
            CmdBuilder(self.home_axis).escape("BR").char().build(),
            CmdBuilder(self.get_status).escape("LM").build(),
            CmdBuilder(self.set_position).escape("B/").spaces().escape("X").int().spaces().escape("Y").int().build(),
            CmdBuilder(self.set_position_as_steps).escape("B").char().int().build()
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
        return "{ACK}{STX}{0},{1}{EOT}".format(x_axis_return, y_axis_return, **COMMAND_CHARS)

    def home_axis(self, axis):
        """
        Home the axis.
        Args:
            axis: acis to home

        Returns: acknowledge when sent

        """
        axis = self.device.axes[axis]
        axis.home()
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
        return "{ACK}{STX}{status}{EOT}".format(status=status, **COMMAND_CHARS)

    def set_position(self, x_position, y_position):
        """
        Set the position in mm * 10^data default
        Args:
            x_position: position for x axis
            y_position: position for y axis

        Returns: acknowledge when done

        """
        self.device.x_axis.sp = x_position
        self.device.y_axis.sp = y_position
        return "{ACK}".format(**COMMAND_CHARS)

    def set_position_as_steps(self, axis, steps):
        """
        Set the position at using increments (steps)
        Args:
            axis: the axis to set
            steps: the number of steps to set it at

        Returns: acknowledgement

        """
        axis = self.device.axes[axis]
        axis.sp = int(steps)
        self.log.info("Setting: Position {}, sp {}".format(axis.rbv, axis.sp))
        return "{ACK}".format(**COMMAND_CHARS)

    def get_position_as_steps(self, axis):
        """
        Get the current position in steps
        Args:
            axis: axis to get the value for

        Returns: the value

        """
        axis = self.device.axes[axis]
        self.log.info("Position {}, sp {}".format(axis.rbv, axis.sp))
        if axis.rbv_error is not None:
            return "{ACK}{STX}{0}{EOT}".format(self.rbv_error, **COMMAND_CHARS)
        else:
            return "{ACK}{STX}{steps:.0f}{EOT}".format(steps=axis.rbv, **COMMAND_CHARS)
