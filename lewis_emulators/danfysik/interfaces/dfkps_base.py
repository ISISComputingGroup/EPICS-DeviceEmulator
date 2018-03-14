"""
Stream device for danfysik
"""
import abc

import six
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder


@has_log
class CommonStreamInterface(object):
    """
    Stream interface for a Danfysik.
    """

    in_terminator = "\r"
    out_terminator = ""

    commands = [
        CmdBuilder("get_voltage").escape("AD 2").eos().build(),
        CmdBuilder("unlock").escape("UNLOCK").eos().build(),
        CmdBuilder("set_polarity").arg("\+|\-").eos().build(),
        CmdBuilder("get_polarity").escape("PO").eos().build(),
        CmdBuilder("set_power_off").escape("F").eos().build(),
        CmdBuilder("set_power_on").escape("N").eos().build(),
        CmdBuilder("get_status").escape("S1").eos().build(),
    ]

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def get_current(self):
        return int(round(self.device.current))

    def set_current(self, value):
        self.device.current = int(value)

    def get_voltage(self):
        return int(round(self.device.voltage))

    def unlock(self):
        """
        Unlock the device. Implementation could be put in in future.
        """

    def get_polarity(self):
        return "-" if self.device.negative_polarity else "+"

    def set_polarity(self, polarity):
        assert polarity in ["+", "-"]
        self.device.negative_polarity = polarity == "-"

    def set_power_off(self):
        self.device.power = False

    def set_power_on(self):
        self.device.power = True

    def get_status(self):
        return ("{pow}" + "." * 21 + "{pow}.").format(
            pow="." if self.device.power else "!"
        )
