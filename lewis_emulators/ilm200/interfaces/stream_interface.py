from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder


@has_log
class Ilm200StreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {

        Cmd("get_version", "^V$"),

        Cmd("get_status", "^X$"),

        Cmd("get_level", "^R1$"),
        Cmd("set_rate_fast", "^T1$"),
        Cmd("set_rate_slow", "^S2$"),
    }

    in_terminator = "\r"
    out_terminator = "\r"

    def __init__(self):

        super(Ilm200StreamInterface, self).__init__()
        self.commands = {
            CmdBuilder(self.get_version).escape("V").build(),
            CmdBuilder(self.get_status).escape("X").build(),
            CmdBuilder(self.get_level).escape("R").int().build(),
            CmdBuilder(self.set_rate_slow).escape("S").int().build(),
            CmdBuilder(self.set_rate_fast).escape("T").int().build(),
        }

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    def get_version(self):
        return "IBEX Emulator"

    def set_rate_slow(self, channel):
        self._device.set_fill_rate(channel=int(channel), fast=False)

    def set_rate_fast(self, channel):
        self._device.set_fill_rate(channel=int(channel), fast=True)

    def get_level(self, channel):
        return self._device.get_level(channel=int(channel))

    def _get_status(self, channel):
        return 0

    def _get_logic_status(self):
        return 0

    def get_status(self):
        d = self._device
        return "X{ch1_type:01d}{ch2_type:01d}{ch3_type:01d}S{ch1_status:02d}{ch2_status:02d}"\
               "{ch3_status:02d}R{logic_status:02d}".format(
                   ch1_type=d.get_cryo_type(1), ch2_type=d.get_cryo_type(2), ch3_type=d.get_cryo_type(3),
                   ch1_status=self._get_status(1), ch2_status=self._get_status(2), ch3_status=self._get_status(3),
                   logic_status=self._get_logic_status()
               )
