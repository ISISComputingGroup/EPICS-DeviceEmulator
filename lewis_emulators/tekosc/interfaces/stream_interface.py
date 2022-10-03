from distutils.command.build import build
from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply

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
            CmdBuilder(self.get_waveform).escape(":DATA:SOURCE CH").int().escape("WAVFRM?").eos().build(),
            CmdBuilder(self.get_outpre).escape(":DATA:SOURCE CH").int().escape("WFMOUTPRE?").eos().build(),
            CmdBuilder(self.get_curve).escape(":DATA:SOURCE CH").int().escape("CURVE?").eos().build(),
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

    def get_waveform(self, channel: int) -> str:
        return self._channel(channel).get_waveform()

    def get_outpre(self, channel: int) -> str:
        return self._channel(channel).preamble

    def get_curve(self, channel: int) -> str:
        return self._channel(channel).curve
