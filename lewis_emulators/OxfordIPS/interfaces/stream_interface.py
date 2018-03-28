from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder


@has_log
class OxfordIPSStreamInterface(StreamInterface):

    in_terminator = "\r"
    out_terminator = "\r"

    def __init__(self):

        super(OxfordIPSStreamInterface, self).__init__()
        self.commands = {
            CmdBuilder(OxfordIPSStreamInterface.get_version).escape("V").build(),
            CmdBuilder(self.get_setpoint_currrent).escape("R5").build(),
            CmdBuilder(self.set_setpoint_currrent).escape("I").float().build(),
        }

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    @staticmethod
    def get_version():
        return "IPS EMULATED"

    def get_setpoint_currrent(self):
        return "R{}".format(self._device.setpoint_current)

    def set_setpoint_currrent(self, value):
        self._device.setpoint_current = value
        return "I"
