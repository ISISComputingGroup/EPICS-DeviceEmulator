from distutils.command.build import build
from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply
from numpy import double

if_connected = conditional_reply("connected")


@has_log
class TekOscStreamInterface(StreamInterface):

    in_terminator = '\n'
    out_terminator = '\n'

    def __init__(self):
        super(TekOscStreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.identity).escape("*IDN?").eos().build(),
            CmdBuilder(self.get_curve).escape(":VERBOSE 0;:HEADER 0;:DATA:SOURCE CH").int().escape(";:DATA:START 1;:DATA:STOP 10000;:DATA:ENC ASCII;:DATA:WIDTH 1;:CURVE?").eos().build(),
            CmdBuilder(self.get_x_incr).escape(":DATA:SOURCE CH").int().escape(";:WFMOUTPRE:XINCR?").eos().build(),
            CmdBuilder(self.get_y_mult).escape(":DATA:SOURCE CH").int().escape(";:WFMOUTPRE:YMULT?").eos().build(),
            CmdBuilder(self.get_x_unit).escape(":DATA:SOURCE CH").int().escape(";:WFMOUTPRE:XUNIT?").eos().build(),
            CmdBuilder(self.get_y_unit).escape(":DATA:SOURCE CH").int().escape(";:WFMOUTPRE:YUNIT?").eos().build(),
            CmdBuilder(self.get_x_zero).escape(":DATA:SOURCE CH").int().escape(";:WFMOUTPRE:XZERO?").eos().build(),
            CmdBuilder(self.get_y_zero).escape(":DATA:SOURCE CH").int().escape(";:WFMOUTPRE:YZERO?").eos().build(),
        }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def identity(self):
        """
        :return: identity of the device
        """
        return "TEKTRONIX,DPO3054,C012754,SCPI:99.0 FV:1.0"

    def _channel(self, channel_num: int):
        """
        Helper method to get a channel object from the device according to number
        """
        return self.device.channels[channel_num]

    def get_curve(self, channel: int) -> str:
        return self._channel(channel).curve

    def get_x_incr(self, channel: int) -> float:
        return self._channel(channel).x_increment

    def get_y_mult(self, channel: int) -> float:
        return self._channel(channel).y_multiplier
    
    def get_x_unit(self, channel: int) -> str:
        return self._channel(channel).x_unit

    def get_y_unit(self, channel: int) -> str:
        return self._channel(channel).y_unit

    def get_x_zero(self, channel: int) -> float:
        return self._channel(channel).x_zero

    def get_y_zero(self, channel:int) -> float:
        return self._channel(channel).y_zero
