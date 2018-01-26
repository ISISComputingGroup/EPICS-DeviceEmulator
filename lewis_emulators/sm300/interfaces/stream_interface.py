"""
Stream interface for the SM 300 motor emulator
"""

from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.constants import EOT, ASCII_CHARS


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

            CmdBuilder(self.home_axis).ack().stx().escape("BR").char().build(),
            CmdBuilder(self.start_movement_to_sp).ack().stx().escape("BSL").build(),
            CmdBuilder(self.stop).ack().stx().escape("BSS").build(),
            CmdBuilder(self.setting).ack().stx().escape("B/").spaces().escape("G").any().build(),
            CmdBuilder(self.set_position).ack().stx().escape("B/").spaces().escape("X").int().spaces().escape("Y").int()
                                         .build(),
            CmdBuilder(self.set_position_as_steps).ack().stx().escape("B").char(not_chars=["FS"]).int().build(),
            CmdBuilder(self.feed_code).ack().stx().escape("BF").int().build(),


            CmdBuilder(self.get_position_as_steps).ack().stx().escape("LI").char().build(),
            CmdBuilder(self.get_status).ack().stx().escape("LM").build(),
            CmdBuilder(self.get_position).ack().stx().escape("LQ").build(),
            CmdBuilder(self.error_status).ack().stx().escape("LS10").build(),

            CmdBuilder(self.disconnect).ack().stx().escape("M").any().build(),

            # This is cheating the PEL1 command comes after PEL0 which is sent with a cr characters so add it in here
            CmdBuilder(self.reset_code).regex(r"\r?").ack().stx().escape("P").any().build()
        }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def generate_reply(self, message=None, override_form_to_eot=False):
        """
        Generate a reply as the device depending on the encoding. There are two choice BCC and EOT form
        EOT is ACK STX <message> EOT and BCC is ACK STX <message> ETX <2 digit checksum>
        Args:
            message: message to send
            override_form_to_eot: If True use the EOT form otherwise use the default form

        Returns: message to reply with.

        """
        if self._device.is_disconnected:
            return None

        if message is None:
            return "{ACK}".format(**ASCII_CHARS)

        if self._device.has_bcc_at_end_of_message and not override_form_to_eot:
            sum_chars = 0
            xor_chars = 0
            for character in str(message):
                as_int = ord(character)
                sum_chars += as_int
                xor_chars ^= as_int
            sum_chars = chr(sum_chars % 256)
            xor_chars = chr(xor_chars)

            reply = "{ACK}{STX}{message}{ETX}{sum}{xor}".format(
                message=message, sum=sum_chars, xor=xor_chars, **ASCII_CHARS)
        else:
            reply = "{ACK}{STX}{message}{EOT}".format(message=message, **ASCII_CHARS)
        return reply

    def get_position(self):
        """
        Get position of the motor axes
        Returns: string indicating position of motors

        """

        x_axis_return = self._device.x_axis.get_label_and_position()
        y_axis_return = self._device.y_axis.get_label_and_position()
        self.log.debug("Send position {} {}".format(x_axis_return, y_axis_return))
        return self.generate_reply("{0},{1}".format(x_axis_return, y_axis_return))

    def home_axis(self, axis):
        """
        Home the axis.
        Args:
            axis: axis to home

        Returns: acknowledge when sent

        """
        axis = self._device.axes[axis]
        axis.home()
        return self.generate_reply()

    def get_status(self):
        """

        Returns: the moving status of the motor, N not at position, P at position, E error

        """
        if self._device.is_moving_error or self._device.error_code is not 0:
            status = "E"
        else:
            is_moving = self._device.is_motor_moving()
            if is_moving:
                status = "N"
            else:
                status = "P"
        self.log.debug("Send motor status {}".format(status))
        return self.generate_reply(status, override_form_to_eot=True)

    def set_position(self, x_position, y_position):
        """
        Set the position in mm * 10^data default
        Args:
            x_position: position for x axis
            y_position: position for y axis

        Returns: acknowledge when done

        """
        self._device.x_axis.sp = x_position
        self._device.y_axis.sp = y_position
        return self.generate_reply()

    def set_position_as_steps(self, axis, steps):
        """
        Set the position at using increments (steps)
        Args:
            axis: the axis to set
            steps: the number of steps to set it at

        Returns: acknowledgement

        """
        axis = self._device.axes[axis]
        axis.sp = int(steps)
        return self.generate_reply()

    def get_position_as_steps(self, axis):
        """
        Get the current position in steps
        Args:
            axis: axis to get the value for

        Returns: the value

        """
        axis = self._device.axes[axis]
        if axis.rbv_error is not None:
            return self.generate_reply(axis.rbv_error)
        else:
            return self.generate_reply("{steps:.0f}".format(steps=axis.rbv))

    def start_movement_to_sp(self):
        """
        Start a movement of all axises to final set points

        Returns: acknowledge

        """
        self._device.move_to_sp()
        return self.generate_reply()

    def reset_code(self, code):
        """
        Record reset codes sent from P commands
        Args:
            code: code from P command

        Returns: acknowledge

        """
        self._device.reset_codes.append("P{}".format(code))
        if code == "EK1":
            self._device.has_bcc_at_end_of_message = False
        elif code == "EK0":
            self._device.has_bcc_at_end_of_message = True
        self.log.info("Reset codes: {}".format(self._device.reset_codes))

        return self.generate_reply()

    def setting(self, code):
        """
        Record reset codes sent from B/ G commands
        Args:
            code: code from P command

        Returns: acknowledge

        """
        self._device.reset_codes.append("B/ G{}".format(code))
        self.log.info("Reset codes: {}".format(self._device.reset_codes))
        return self.generate_reply()

    def feed_code(self, code):
        """
        Record reset codes sent from BF commands
        Args:
            code: code from P command

        Returns: acknowledge

        """
        self._device.reset_codes.append("BF{}".format(code))
        self.log.info("Reset codes: {}".format(self._device.reset_codes))
        return self.generate_reply()

    def stop(self):
        """
        Stops all axes movement
        Returns: acknowledge

        """
        for axis in self._device.axes.values():
            axis.stop()

        return self.generate_reply("P")

    def disconnect(self, code):
        """
        Command to disconnect from the device
        Args:
            code: code called with

        Returns: No response

        """
        self._device.disconnect = code
        return None

    def error_status(self):
        """
        Returns: the current error code
        """
        error_code = "{:02x}".format(self._device.error_code)
        self.log.debug("error code {}".format(error_code))
        return self.generate_reply(error_code)
