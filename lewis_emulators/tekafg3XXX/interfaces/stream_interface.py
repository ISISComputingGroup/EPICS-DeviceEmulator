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
            CmdBuilder(self.identity).escape("*IDN?").eos().build(),
            CmdBuilder(self.trigger).escape("*TRG").eos().build(),
            CmdBuilder(self.get_status).escape("OUTP").int().escape(":STAT?").build(),
            CmdBuilder(self.set_status).escape("OUTP").int().escape(":STAT ").int().build(),
            CmdBuilder(self.get_function).escape("SOUR").int().escape(":FUNC:SHAP?").build(),
            CmdBuilder(self.set_function).escape("SOUR").int().escape(":FUNC:SHAP ").arg("SIN|SQU|PULS|RAMP|PRN|DC|SINC|GAUS|LOR|ERIS|EDEC|HAV").build(),
            CmdBuilder(self.get_polarity).escape("OUTP").int().escape(":POL?").build(),
            CmdBuilder(self.set_polarity).escape("OUTP").int().escape(":POL ").arg("NORM|INV").build(),
            CmdBuilder(self.get_impedance).escape("OUTP").int().escape(":IMP?").build(),
            CmdBuilder(self.set_impedance).escape("OUTP").int().escape(":IMP ").float().build(),
            CmdBuilder(self.get_voltage).escape("SOUR").int().escape(":VOLT?").build(),
            CmdBuilder(self.set_voltage).escape("SOUR").int().escape(":VOLT ").float().build(),
            CmdBuilder(self.get_voltage_units).escape("SOUR").int().escape(":VOLT:UNIT?").build(),
            CmdBuilder(self.set_voltage_units).escape("SOUR").int().escape(":VOLT:UNIT ").arg("VPP|VRMS|DBM").build(),
            CmdBuilder(self.get_voltage_low_level).escape("SOUR").int().escape(":VOLT:LEV:IMM:LOW?").build(),
            CmdBuilder(self.set_voltage_low_level).escape("SOUR").int().escape(":VOLT:LEV:IMM:LOW ").float().build(),
            CmdBuilder(self.get_voltage_high_level).escape("SOUR").int().escape(":VOLT:LEV:IMM:HIGH?").build(),
            CmdBuilder(self.set_voltage_high_level).escape("SOUR").int().escape(":VOLT:LEV:IMM:HIGH ").float().build(),
            CmdBuilder(self.get_voltage_low_limit).escape("SOUR").int().escape(":VOLT:LIM:LOW?").build(),
            CmdBuilder(self.set_voltage_low_limit).escape("SOUR").int().escape(":VOLT:LIM:LOW ").float().build(),
            CmdBuilder(self.get_voltage_high_limit).escape("SOUR").int().escape(":VOLT:LIM:HIGH?").build(),
            CmdBuilder(self.set_voltage_high_limit).escape("SOUR").int().escape(":VOLT:LIM:HIGH ").float().build(),
            CmdBuilder(self.get_voltage_offset).escape("SOUR").int().escape(":VOLT:LEV:IMM:OFFS?").build(),
            CmdBuilder(self.set_voltage_offset).escape("SOUR").int().escape(":VOLT:LEV:IMM:OFFS ").float().build(),
            CmdBuilder(self.get_frequency).escape("SOUR").int().escape(":FREQ:FIX?").build(),
            CmdBuilder(self.set_frequency).escape("SOUR").int().escape(":FREQ:FIX ").float().build(),
            CmdBuilder(self.get_phase).escape("SOUR").int().escape(":PHASE:ADJ?").build(),
            CmdBuilder(self.set_phase).escape("SOUR").int().escape(":PHASE:ADJ ").float().build(),
            CmdBuilder(self.get_burst_status).escape("SOUR").int().escape(":BURS:STAT?").build(),
            CmdBuilder(self.set_burst_status).escape("SOUR").int().escape(":BURS:STAT ").arg("ON|OFF|1|0").build(),
            CmdBuilder(self.get_burst_mode).escape("SOUR").int().escape(":BURS:MODE?").build(),
            CmdBuilder(self.set_burst_mode).escape("SOUR").int().escape(":BURS:MODE ").arg("TRIG|GAT").build(),
            CmdBuilder(self.get_burst_num_cycles).escape("SOUR").int().escape(":BURS:NCYC?").build(),
            CmdBuilder(self.set_burst_num_cycles).escape("SOUR").int().escape(":BURS:NCYC ").float().build(),
            CmdBuilder(self.get_burst_time_delay).escape("SOUR").int().escape(":BURS:TDEL?").build(),
            CmdBuilder(self.set_burst_time_delay).escape("SOUR").int().escape(":BURS:TDEL ").float().build(),
            CmdBuilder(self.get_frequency_mode).escape("SOUR").int().escape(":FREQ:MODE?").build(),
            CmdBuilder(self.set_frequency_mode).escape("SOUR").int().escape(":FREQ:MODE ").arg("CW|FIX|SWE").build(),
            CmdBuilder(self.get_sweep_span).escape("SOUR").int().escape(":FREQ:SPAN?").build(),
            CmdBuilder(self.set_sweep_span).escape("SOUR").int().escape(":FREQ:SPAN ").float().build(),
            CmdBuilder(self.get_sweep_start).escape("SOUR").int().escape(":FREQ:STAR?").build(),
            CmdBuilder(self.set_sweep_start).escape("SOUR").int().escape(":FREQ:STAR ").float().build(),
            CmdBuilder(self.get_sweep_stop).escape("SOUR").int().escape(":FREQ:STOP?").build(),
            CmdBuilder(self.set_sweep_stop).escape("SOUR").int().escape(":FREQ:STOP ").float().build(),
            CmdBuilder(self.get_sweep_hold_time).escape("SOUR").int().escape(":SWE:HTIM?").build(),
            CmdBuilder(self.set_sweep_hold_time).escape("SOUR").int().escape(":SWE:HTIM ").float().build(),
            CmdBuilder(self.get_sweep_mode).escape("SOUR").int().escape(":SWE:MODE?").build(),
            CmdBuilder(self.set_sweep_mode).escape("SOUR").int().escape(":SWE:MODE ").arg("AUTO|MAN").build(),
            CmdBuilder(self.get_sweep_return_time).escape("SOUR").int().escape(":SWE:RTIM?").build(),
            CmdBuilder(self.set_sweep_return_time).escape("SOUR").int().escape(":SWE:RTIM ").float().build(),
            CmdBuilder(self.get_sweep_spacing).escape("SOUR").int().escape(":SWE:SPAC?").build(),
            CmdBuilder(self.set_sweep_spacing).escape("SOUR").int().escape(":SWE:SPAC ").arg("LIN|LOG").build(),
            CmdBuilder(self.get_sweep_time).escape("SOUR").int().escape(":SWE:TIME?").build(),
            CmdBuilder(self.set_sweep_time).escape("SOUR").int().escape(":SWE:TIME ").float().build(),
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

    def trigger(self):
        self.device.triggered = True

    def _channel(self, channel_num: int):
        """
        Helper method to get a channel object from the device according to number
        """
        return self.device.channels[channel_num]

    def get_status(self, channel: int) -> int:
        return self._channel(channel).status

    def set_status(self, channel: int, new_status: int):
        self._channel(channel).status = new_status

    def get_function(self, channel: int) -> str:
        return self._channel(channel).function

    def set_function(self, channel: int, new_function: str):
        self._channel(channel).function = new_function

    def get_polarity(self, channel: int) -> str:
        return self._channel(channel).polarity

    def set_polarity(self, channel: int, new_polarity: str):
        self._channel(channel).polarity = new_polarity

    def get_impedance(self, channel: int) -> float:
        return self._channel(channel).impedance

    def set_impedance(self, channel: int, new_impedance: float):
        self._channel(channel).impedance = new_impedance

    def get_voltage(self, channel: int) -> int:
        return self._channel(channel).voltage

    def set_voltage(self, channel: int, new_voltage: float):
        self._channel(channel).voltage = new_voltage

    def get_voltage_units(self, channel: int) -> str:
        return self._channel(channel).voltage_units

    def set_voltage_units(self, channel: int, new_voltage_units: str):
        self._channel(channel).voltage_units = new_voltage_units

    def get_voltage_low_limit(self, channel: int) -> float:
        return self._channel(channel).voltage_low_limit

    def set_voltage_low_limit(self, channel: int, new_voltage_low_limit: float):
        self._channel(channel).voltage_low_limit = new_voltage_low_limit

    def get_voltage_low_level(self, channel: int) -> float:
        return self._channel(channel).voltage_low_level

    def set_voltage_low_level(self, channel: int, new_voltage_low_level: float):
        self._channel(channel).voltage_low_level = new_voltage_low_level

    def get_voltage_high_limit(self, channel: int) -> float:
        return self._channel(channel).voltage_high_limit

    def set_voltage_high_limit(self, channel: int, new_voltage_high_limit: float):
        self._channel(channel).voltage_high_limit = new_voltage_high_limit

    def get_voltage_high_level(self, channel: int) -> float:
        return self._channel(channel).voltage_high_level

    def set_voltage_high_level(self, channel: int, new_voltage_high_level: float):
        self._channel(channel).voltage_high_level = new_voltage_high_level

    def get_voltage_offset(self, channel: int) -> float:
        return self._channel(channel).voltage_offset

    def set_voltage_offset(self, channel: int, new_voltage_offset: float):
        self._channel(channel).voltage_offset = new_voltage_offset

    def get_frequency(self, channel: int) -> float:
        return self._channel(channel).frequency

    def set_frequency(self, channel: int, new_frequency: float):
        self._channel(channel).frequency = new_frequency

    def get_frequency_mode(self, channel: int) -> str:
        return self._channel(channel).frequency_mode

    def set_frequency_mode(self, channel: int, new_frequency_mode: str):
        self._channel(channel).frequency_mode = new_frequency_mode

    def get_phase(self, channel: int) -> float:
        return self._channel(channel).frequency

    def set_phase(self, channel: int, new_phase: float):
        self._channel(channel).phase = new_phase

    def get_burst_status(self, channel: int) -> str:
        return 1 if self._channel(channel).burst_status == "ON" else 0

    def set_burst_status(self, channel: int, new_burst_status: str):
        self._channel(channel).burst_status = new_burst_status

    def get_burst_mode(self, channel: int) -> str:
        return self._channel(channel).burst_mode

    def set_burst_mode(self, channel: int, new_burst_mode: str):
        self._channel(channel).burst_mode = new_burst_mode

    def get_burst_num_cycles(self, channel: int) -> int:
        return self._channel(channel).burst_num_cycles

    def set_burst_num_cycles(self, channel: int, new_burst_num_cycles: int):
        self._channel(channel).burst_num_cycles = new_burst_num_cycles

    def get_burst_time_delay(self, channel: int) -> int:
        return self._channel(channel).burst_time_delay

    def set_burst_time_delay(self, channel: int, new_burst_time_delay: int):
        self._channel(channel).burst_time_delay = new_burst_time_delay

    def get_sweep_span(self, channel: int) -> int:
        return self._channel(channel).sweep_span

    def set_sweep_span(self, channel: int, new_sweep_span: int):
        self._channel(channel).sweep_span = new_sweep_span

    def get_sweep_start(self, channel: int) -> int:
        return self._channel(channel).sweep_start

    def set_sweep_start(self, channel: int, new_sweep_start: int):
        self._channel(channel).sweep_start = new_sweep_start

    def get_sweep_stop(self, channel: int) -> int:
        return self._channel(channel).sweep_stop

    def set_sweep_stop(self, channel: int, new_sweep_stop: int):
        self._channel(channel).sweep_stop = new_sweep_stop

    def get_sweep_hold_time(self, channel: int) -> int:
        return self._channel(channel).sweep_hold_time

    def set_sweep_hold_time(self, channel: int, new_sweep_hold_time: int):
        self._channel(channel).sweep_hold_time = new_sweep_hold_time

    def get_sweep_mode(self, channel: int) -> str:
        return self._channel(channel).sweep_mode

    def set_sweep_mode(self, channel: int, new_sweep_mode: str):
        self._channel(channel).sweep_mode = new_sweep_mode

    def get_sweep_return_time(self, channel: int) -> int:
        return self._channel(channel).sweep_return_time

    def set_sweep_return_time(self, channel: int, new_sweep_return_time: int):
        self._channel(channel).sweep_return_time = new_sweep_return_time

    def get_sweep_spacing(self, channel: int) -> str:
        return self._channel(channel).sweep_spacing

    def set_sweep_spacing(self, channel: int, new_sweep_spacing: str):
        self._channel(channel).sweep_spacing = new_sweep_spacing

    def get_sweep_time(self, channel: int) -> int:
        return self._channel(channel).sweep_time

    def set_sweep_time(self, channel: int, new_sweep_time: int):
        self._channel(channel).sweep_time = new_sweep_time
