from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log


@has_log
class Ilm200StreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_channel_1_level", "^R1$"),
        Cmd("get_channel_2_level", "^R2$"),
        Cmd("get_channel_3_level", "^R3$"),

        Cmd("get_version", "^V$"),

        Cmd("set_channel_1_fast", "^T1$"),
        Cmd("set_channel_2_fast", "^T2$"),
        Cmd("set_channel_3_fast", "^T3$"),
        Cmd("set_channel_1_slow", "^S1$"),
        Cmd("set_channel_2_slow", "^S2$"),
        Cmd("set_channel_3_slow", "^S3$"),
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    def get_version(self):
        return "IBEX Emulator"

    def get_channel_1_level(self):
        return self._device.get_level(channel=1)

    def get_channel_2_level(self):
        return self._device.get_level(channel=2)

    def get_channel_3_level(self):
        return self._device.get_level(channel=3)

    def set_channel_1_fast(self):
        self._device.set_rate(channel=1, fast=True)

    def set_channel_2_fast(self):
        self._device.set_rate(channel=2, fast=True)

    def set_channel_3_fast(self):
        self._device.set_rate(channel=3, fast=True)

    def set_channel_1_slow(self):
        self._device.set_rate(channel=1, fast=False)

    def set_channel_2_slow(self):
        self._device.set_rate(channel=2, fast=False)

    def set_channel_3_slow(self):
        self._device.set_rate(channel=3, fast=False)