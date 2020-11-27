"""
Stream device for danfysik
"""
import abc
import six

from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_available = conditional_reply("device_available")


@has_log
@six.add_metaclass(abc.ABCMeta)
class CommonStreamInterface(object):
    """
    Common part of the stream interface for a Danfysik.
    """

    in_terminator = "\r"
    out_terminator = ""

    commands = [
        CmdBuilder("get_voltage").escape("AD 2").eos().build(),
        CmdBuilder("set_polarity").arg("\+|\-").eos().build(),
        CmdBuilder("get_polarity").escape("PO").eos().build(),
        CmdBuilder("set_power_off").escape("F").eos().build(),
        CmdBuilder("set_power_on").escape("N").eos().build(),
        CmdBuilder("get_status").escape("S1").eos().build(),
        CmdBuilder("get_last_setpoint").escape("RA").eos().build(),
        CmdBuilder("reset").escape("RS").eos().build(),
    ]

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem
        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    @conditional_reply("device_available")
    @conditional_reply("comms_initialized")
    def get_current(self):
        return int(round(self.device.get_current()))

    @conditional_reply("comms_initialized")
    def set_current(self, value):
        self.device.set_current(value)

    @conditional_reply("comms_initialized")
    def get_last_setpoint(self):
        return int(round(self.device.get_last_setpoint()))

    @conditional_reply("device_available")
    @conditional_reply("comms_initialized")
    def get_voltage(self):
        return int(round(self.device.get_voltage()))

    @conditional_reply("comms_initialized")
    def unlock(self):
        """
        Unlock the device. Implementation could be put in in future.
        """

    @conditional_reply("comms_initialized")
    def get_polarity(self):
        return "-" if self.device.negative_polarity else "+"

    @conditional_reply("comms_initialized")
    def set_polarity(self, polarity):
        assert polarity in ["+", "-"]
        self.device.negative_polarity = polarity == "-"

    @conditional_reply("comms_initialized")
    def set_power_off(self):
        self.device.power = False

    @conditional_reply("comms_initialized")
    def set_power_on(self):
        self.device.power = True

    @conditional_reply("comms_initialized")
    def reset_device(self):
        self.device.reset()

    @abc.abstractmethod
    def get_status(self):
        """
        Respond to the get_status command.
        """
    @if_available
    def init_comms(self):
        """
        Initialize comms of device
        """
        self.device.comms_initialized = True
