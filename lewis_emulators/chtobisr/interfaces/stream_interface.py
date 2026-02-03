from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply


@has_log
class ChtobisrStreamInterface(StreamInterface):
    """Stream interface for the Coherent OBIS Laser Remote
    """

    commands = {
        CmdBuilder("get_id").escape("*IDN").int().escape("?").eos().build(),
        CmdBuilder("set_reset").escape("*RST").int().eos().build(),
        CmdBuilder("get_interlock").escape("SYSTEM").int().escape(":LOCK?").eos().build(),
        CmdBuilder("get_status").escape("SYSTEM").int().escape(":STATUS?").eos().build(),
        CmdBuilder("get_faults").escape("SYSTEM").int().escape(":FAULT?").eos().build(),
        CmdBuilder("get_power").escape("SOURce").int().escape(":POWer:LEVel:IMMediate:AMPLitude?").eos().build(),
        CmdBuilder("get_state").escape("SOURce").int().escape(":AM:STATe?").eos().build(),
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        """If command is not recognised, print and error

        Args:
            request: requested string
            error: problem
        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    @conditional_reply("connected")
    def get_id(self, addr: int):
        """Gets the device Identification string

        :return:  Device ID string
        """
        return "{}".format(self._device.id)

    @conditional_reply("connected")
    def set_reset(self, addr: int):
        """Resets the device

        :return:  none
        """
        self._device.reset()

    @conditional_reply("connected")
    def get_interlock(self, addr: int):
        """Gets the device interlock status

        :return: Interlock status
        """
        return "{}".format(self._device.interlock)

    @conditional_reply("connected")
    def get_status(self, addr: int):
        """Returns status code
        :return: Formatted status code
        """
        return "{:08X}".format(self._device.build_status_code())

    @conditional_reply("connected")
    def get_faults(self, addr: int):
        """Returns faults code
        :return: Formatted fault code
        """
        return "{:08X}".format(self._device.build_fault_code())

    def get_power(self, addr: int):
        return "0.0"

    def get_state(self, addr: int):
        return "OFF"
