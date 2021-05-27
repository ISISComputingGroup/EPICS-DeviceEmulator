from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


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

    def _channel(self, channel):
        return self.device.channels[channel]

    @property
    def status(self, channel: int) -> str:
        return self._channel(channel).status

    @status.setter
    def status(self, channel: int, new_status: str):
        self._channel(channel).status = new_status

    @property
    def polarity(self, channel: int) -> str:
        return self._channel(channel).polarity

    @polarity.setter
    def polarity(self, channel: int, new_polarity: str):
        self._channel(channel).polarity = new_polarity

    @property
    def burst_status(self, channel: int) -> str:
        return self._channel(channel).burst_status

    @burst_status.setter
    def burst_status(self, channel: int, new_burst_status: str):
        self._channel(channel).burst_status = new_burst_status

    @property
    def burst_mode(self, channel: int) -> str:
        return self._channel(channel).burst_mode

    @burst_mode.setter
    def burst_mode(self, channel: int, new_burst_mode: str):
        self._channel(channel).burst_mode = new_burst_mode

    @property
    def impedance(self, channel: int) -> float:
        return self._channel(channel).impedance

    @impedance.setter
    def impedance(self, channel: int, new_impedance: float):
        self._channel(channel).impedance = new_impedance

    @property
    def voltage(self, channel: int) -> int:
        return self._channel(channel).voltage

    @voltage.setter
    def voltage(self, channel: int, new_voltage: float):
        self._channel(channel).voltage = new_voltage

    @property
    def voltage_units(self, channel: int) -> str:
        return self._channel(channel).voltage_units

    @voltage_units.setter
    def voltage_units(self, channel: int, new_voltage_units: str):
        self._channel(channel).voltage_units = new_voltage_units

    @property
    def voltage_low_limit(self, channel: int) -> float:
        return self._channel(channel).voltage_low_limit

    @voltage_low_limit.setter
    def voltage_low_limit(self, channel: int, new_voltage_low_limit: float):
        self._channel(channel).voltage_low_limit = new_voltage_low_limit

    @property
    def voltage_low_level(self, channel: int) -> float:
        return self._channel(channel).voltage_low_level

    @voltage_low_level.setter
    def voltage_low_level(self, channel: int, new_voltage_low_level: float):
        self._channel(channel).voltage_low_level = new_voltage_low_level

    @property
    def voltage_high_limit(self, channel: int) -> float:
        return self._channel(channel).voltage_high_limit

    @voltage_high_limit.setter
    def voltage_high_limit(self, channel: int, new_voltage_high_limit: float):
        self._channel(channel).voltage_high_limit = new_voltage_high_limit

    @property
    def voltage_high_level(self, channel: int) -> float:
        return self._channel(channel).voltage_high_level

    @voltage_high_level.setter
    def voltage_high_level(self, channel: int, new_voltage_high_level: float):
        self._channel(channel).voltage_high_level = new_voltage_high_level

    @property
    def voltage_offset(self, channel: int) -> float:
        return self._channel(channel).voltage_offset

    @voltage_offset.setter
    def voltage_offset(self, channel: int, new_voltage_offset: float):
        self._channel(channel).voltage_offset = new_voltage_offset

    @property
    def frequency(self, channel: int) -> float:
        return self._channel(channel).frequency

    @frequency.setter
    def frequency(self, channel: int, new_frequency: float):
        self._channel(channel).frequency = new_frequency

    @property
    def phase(self, channel: int) -> float:
        return self._channel(channel).frequency

    @phase.setter
    def phase(self, channel: int, new_phase: float):
        self._channel(channel).phase = new_phase



