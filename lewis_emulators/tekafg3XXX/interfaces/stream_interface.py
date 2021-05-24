from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")
STATUS_MAP = {True: "ON", False: "OFF"}
POLARITY_MAP = {True: "NORM", False: "INV"}
BURST_MODE_MAP = {True: "TRIG", False: "GAT"}


@has_log
class Tekafg3XXXStreamInterface(StreamInterface):

    in_terminator = '\n'
    out_terminator = '\n'

    def __init__(self):
        super(Tekafg3XXXStreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.identity).escape("*IDN?").eos().build()
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
        return "TEKTRONIX,AFG3021,C100101,SCPI:99.0 FV:1.0"

    @property
    def status(self):
        return STATUS_MAP[self.device.status]

    @status.setter
    def status(self, new_status: str):
        self.device.status = next(key for key, value in STATUS_MAP.items() if value == new_status)

    @property
    def polarity(self):
        return POLARITY_MAP[self.device.normal_polarity]

    @polarity.setter
    def polarity(self, new_polarity: str):
        self.device.normal_polarity = next(key for key, value in POLARITY_MAP.items() if value == new_polarity)

    @property
    def burst_status(self):
        return STATUS_MAP[self.device.burst_on]

    @burst_status.setter
    def burst_status(self, new_burst_status: str):
        self.device.burst_on = next(key for key, value in STATUS_MAP.items() if value == new_burst_status)

    @property
    def burst_mode(self):
        return STATUS_MAP[self.device.burst_triggered]

    @burst_mode.setter
    def burst_mode(self, new_burst_mode: str):
        self.device.burst_triggered = next(key for key, value in BURST_MODE_MAP.items() if value == new_burst_mode)
