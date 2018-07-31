from lewis.adapters.stream import StreamInterface, Cmd
from lewis_emulators.utils.command_builder import CmdBuilder


class OmibthxStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_humidity").escape("*SRH2").eos().build(),
        CmdBuilder("get_temperature").escape("*SRTC").eos().build(),
        CmdBuilder("get_pressure").escape("*SRHb").eos().build(),
        CmdBuilder("get_dewpoint").escape("*SRDC2").eos().build(),
    }

    def get_humidity(self):
        return "{:.1f}".format(self.device.humidity)

    def get_temperature(self):
        return "{:.2f}".format(self.device.temperature)

    def get_pressure(self):
        return "{:.2f}".format(self.device.pressure)

    def get_dewpoint(self):
        return "{:.2f}".format(self.device.dew_point)
