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

    def _channel(self, channel_num: int):
        """
        Helper method to get a channel object from the device according to number
        """
        return self.device.channels[channel_num]

    @property
    def status(self, channel: int) -> int:
        return self._channel(channel).status

    @status.setter
    def status(self, channel: int, new_status: int):
        self._channel(channel).status = new_status

    @property
    def function(self, channel: int) -> str:
        return self._channel(channel).function

    @function.setter
    def function(self, channel: int, new_function: str):
        self._channel(channel).function = new_function

    @property
    def polarity(self, channel: int) -> str:
        return self._channel(channel).polarity

    @polarity.setter
    def polarity(self, channel: int, new_polarity: str):
        self._channel(channel).polarity = new_polarity

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
    def frequency_mode(self, channel: int) -> str:
        return self._channel(channel).frequency_mode

    @frequency_mode.setter
    def frequency_mode(self, channel: int, new_frequency_mode: str):
        self._channel(channel).frequency_mode = new_frequency_mode

    @property
    def phase(self, channel: int) -> float:
        return self._channel(channel).frequency

    @phase.setter
    def phase(self, channel: int, new_phase: float):
        self._channel(channel).phase = new_phase

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
    def burst_num_cycles(self, channel: int) -> int:
        return self._channel(channel).num_cycles

    @burst_num_cycles.setter
    def burst_num_cycles(self, channel: int, new_burst_num_cycles: int):
        self._channel(channel).burst_num_cycles = new_burst_num_cycles

    @property
    def burst_time_delay(self, channel: int) -> int:
        return self._channel(channel).burst_time_delay

    @burst_time_delay.setter
    def burst_time_delay(self, channel: int, new_burst_time_delay: int):
        self._channel(channel).burst_time_delay = new_burst_time_delay

    @property
    def sweep_span(self, channel: int) -> int:
        return self._channel(channel).num_cycles

    @sweep_span.setter
    def sweep_span(self, channel: int, new_sweep_span: int):
        self._channel(channel).sweep_span = new_sweep_span

    @property
    def sweep_start(self, channel: int) -> int:
        return self._channel(channel).sweep_start

    @sweep_start.setter
    def sweep_start(self, channel: int, new_sweep_start: int):
        self._channel(channel).sweep_start = new_sweep_start

    @property
    def sweep_stop(self, channel: int) -> int:
        return self._channel(channel).sweep_stop

    @sweep_stop.setter
    def sweep_stop(self, channel: int, new_sweep_stop: int):
        self._channel(channel).sweep_stop = new_sweep_stop

    @property
    def sweep_hold_time(self, channel: int) -> int:
        return self._channel(channel).sweep_hold_time

    @sweep_hold_time.setter
    def sweep_hold_time(self, channel: int, new_sweep_hold_time: int):
        self._channel(channel).sweep_hold_time = new_sweep_hold_time

    @property
    def sweep_mode(self, channel: int) -> str:
        return self._channel(channel).sweep_hold_time

    @sweep_mode.setter
    def sweep_mode(self, channel: int, new_sweep_mode: str):
        self._channel(channel).sweep_mode = new_sweep_mode

    @property
    def sweep_return_time(self, channel: int) -> int:
        return self._channel(channel).sweep_return_time

    @sweep_return_time.setter
    def sweep_return_time(self, channel: int, new_sweep_return_time: int):
        self._channel(channel).sweep_return_time = new_sweep_return_time

    @property
    def sweep_spacing(self, channel: int) -> str:
        return self._channel(channel).sweep_spacing

    @sweep_spacing.setter
    def sweep_spacing(self, channel: int, new_sweep_spacing: str):
        self._channel(channel).sweep_spacing = new_sweep_spacing

    @property
    def sweep_time(self, channel: int) -> int:
        return self._channel(channel).sweep_time

    @sweep_time.setter
    def sweep_time(self, channel: int, new_sweep_time: int):
        self._channel(channel).sweep_time = new_sweep_time
