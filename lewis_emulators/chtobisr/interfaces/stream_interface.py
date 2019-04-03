from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply


@has_log
class ChtobisrStreamInterface(StreamInterface):

    """
    Stream interface for the Coherent OBIS Laser Remote
    """

    commands = {
        CmdBuilder("get_id").escape("*IDN?").build()
        #CmdBuilder("get_status").escape("SYSTEM:STATUS?").build(),
        #CmdBuilder("get_faults").escape("SYSTEM:FAULT?").build(),
        #CmdBuilder("get_interlock").escape("SYSTEM:LOCK?").build(),
        #CmdBuilder("set_reset").escape("*RST").build()
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):

        """
        If command is not recognised, print and error

        Args:
            request: requested string
            error: problem
        """

        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    @conditional_reply("connected")
    def get_id(self):

        """
        Gets the device Identification string

        :return:  Device ID string
        """

        device = self._device
        return "{}".format(device.id)
