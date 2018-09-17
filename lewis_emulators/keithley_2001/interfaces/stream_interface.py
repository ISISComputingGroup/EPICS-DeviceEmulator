from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.keithley_2001.utils import MEASUREMENT_TYPE, BUFFER_CONTROL_MODE, BUFFER_SOURCE, TIMESTAMP_FORMAT
from lewis_emulators.keithley_2001.utils import CONTROL_SOURCE, SCAN_STATE


class Keithley_2001StreamInterface(StreamInterface):

    in_terminator = "\n"
    out_terminator = "\n"

    commands = {
        CmdBuilder("get_idn").escape("*IDN?").build(),
        CmdBuilder("empty_error_queue").escape(":SYST:CLE").build(),

        CmdBuilder("set_measurement").escape(":FUNC ").arg(
            "VOLT:DC|VOLT:AC|CURR:DC|CURR:AC|RES|FRES||FREQ|TEMP").build(),
        CmdBuilder("get_measurement").escape(":FUNC?").build(),

        CmdBuilder("clear_buffer").escape("TRAC:CLE").build(),
        CmdBuilder("set_buffer_source").escape("TRAC:FEED ").arg("SENS|CALC|NONE").build(),
        CmdBuilder("set_buffer_control_mode").escape("TRAC:FEED:CONT ").arg("NEV|NEXT|ALW").build(),
        CmdBuilder("get_buffer_status").escape("TRAC:FREE?").build(),
        CmdBuilder("get_buffer_readings").escape("TRAC:DATA?").int().escape(",").int().build(),
        CmdBuilder("set_buffer_size").escape("TRAC:POIN ").int().build(),
        CmdBuilder("get_buffer_size").escape("TRAC:POIN?").build(),

        CmdBuilder("get_delay").escape("TRIG:DEL?").build(),
        CmdBuilder("set_delay").escape("TRIG:DEL ").float().build(),

        CmdBuilder("set_continuous_init_state").escape("INIT:CONT ").arg("OFF|ON").build(),
        CmdBuilder("get_continuous_init_state").escape("INIT:CONT?").build(),

        CmdBuilder("set_event_control_source").escape("TRIG:SOUR ").arg("HOLD|IMM|MAN|BUS|TLIN|EXT|TIM").build(),
        CmdBuilder("get_event_control_source").escape("TRIG:SOUR?").build(),

        CmdBuilder("set_readback_elements").escape("FORM:ELEM READ, CHAN, UNIT, TIME").build(),
        CmdBuilder("get_readback_elements").escape("FORM:ELEM?").build(),

        CmdBuilder("set_unit_range").arg("VOLT:AC|VOLT:DC|RES|FRES|CURR:AC|CURR:DC").escape(":RANG ").int().build(),
        CmdBuilder("get_unit_range").arg("VOLT:AC|VOLT:DC|RES|FRES|CURR:AC|CURR:DC").escape(":RANG?").build(),

        CmdBuilder("set_unit_auto_range_status").arg("VOLT:AC|VOLT:DC|RES|FRES|CURR:AC|CURR:DC")
            .escape(":RANG:AUTO ").arg("0|1|ONCE").build(),
        CmdBuilder("get_unit_auto_range_status").arg("VOLT:AC|VOLT:DC|RES|FRES|CURR:AC|CURR:DC")
            .escape(":RANG:AUTO?").build(),

        CmdBuilder("set_unit_resolution").arg("VOLT:AC|VOLT:DC|RES|FRES|CURR:AC|CURR:DC")
            .escape("DIG ").arg("4|5|6|7|8|9|DEF|MIN|MAX").build(),

        CmdBuilder("set_unit_rate").arg("VOLT:AC|VOLT:DC|RES|FRES|CURR:AC|CURR:DC")
            .escape(":NPLC ").arg("%f|DEF|MIN|MAX").build(),

        CmdBuilder("set_scan_state").escape("ROUT:SCAN:LSEL ").arg("INT|EXT|RAT|DELT|NONE").build(),
        CmdBuilder("get_scan_state").escape("ROUT:SCAN:LSEL?").build(),

        CmdBuilder("set_channels_to_scan", arg_sep="").escape("ROUT:SCAN (@").int().escape(":").int().escape(
            ")").build(),
        CmdBuilder("get_channels_to_scan").escape("ROUT:SCAN?").build(),

        CmdBuilder("abort").escape("ABOR").build()
    }

    def handle_error(self, request, error):
        self.log.error("An error occurred at request {}: {}".format(repr(request), repr(error)))
        print("An error occurred at request {}: {}".format(repr(request),repr(error)))

    def bool_on_off_value(self, string_value):
        if string_value not in ["ON", "OFF"]:
            raise ValueError("Invalid on/off value!")
        else:
            if string_value == "ON":
                return True
            else:
                return False

    def enum_on_off_value(self, bool_value):
        if bool_value not in [True, False]:
            raise ValueError("Invalid on/off value!")
        else:
            if bool_value:
                return 1
            else:
                return 0

    def get_idn(self):
        return self._device.idn

    def empty_error_queue(self):
        self.log.info("Error log emptied")

    def clear_buffer(self):
        self._device.buffer = ""

    def set_measurement(self, measurement):
        if measurement in MEASUREMENT_TYPE.values():
            self._device.measurement = MEASUREMENT_TYPE.keys()[MEASUREMENT_TYPE.values().index(measurement)]
        else:
            raise ValueError("Invalid measurement value!")

    def get_measurement(self):
        return "\"{}\"".format(MEASUREMENT_TYPE[self._device.measurement])

    def set_buffer_source(self, feed):
        if feed in BUFFER_SOURCE.values():
            self._device.buffer_feed = BUFFER_SOURCE.keys()[BUFFER_SOURCE.values().index(feed)]
        else:
            raise ValueError("Invalid feed source value!")

    def set_buffer_control_mode(self, control):
        if control in BUFFER_SOURCE.values():
            self._device.buffer_control = BUFFER_CONTROL_MODE.keys()[BUFFER_CONTROL_MODE.values().index(control)]
        else:
            raise ValueError("Invalid buffer control source value!")

    def get_buffer_status(self):
        """
        :return: String containing number of bytes available, and number of bytes used
        """
        return "{}, {}".format(str(self._device.bytes_available), str(self._device.bytes_used))

    def get_buffer_readings(self):
        """
        :param count: Number of buffer values to retrieve
        :return: String value of readings from buffer

        Rewrite this!!!!!!!
        """
        self._device.buffer_range_readings = ""
        for i in range(int(count)):
            if int(self._device.current_buffer_loc) >= len(self._device.buffer_full):
                self._device.next_buffer_location = len(
                    self._device.buffer_full) - self._device.current_buffer_loc + i
                self._device.current_buffer_loc = 0
                self._device.fill_buffer()
            else:
                next_reading = str(self._device.buffer_full[int(self._device.current_buffer_loc)])
                self._device.current_buffer_loc += 1
                self._device.buffer_range_readings += next_reading
        return self._device.buffer_range_readings

    def set_buffer_size(self, size):
        self._device.buffer_size = size

    def get_buffer_size(self):
        return self._device.buffer_size

    def set_time_stamp_format(self, format):
        if format in TIMESTAMP_FORMAT.values():
            self._device.time_stamp_format = TIMESTAMP_FORMAT.keys()[TIMESTAMP_FORMAT.values().index(format)]
        else:
            raise ValueError("Invalid timestamp format value")

    def get_time_stamp_format(self):
        return TIMESTAMP_FORMAT[self._device.time_stamp_format]

    def get_delay_state(self):
        return self.enum_onoff_value(self._device.auto_delay_on)

    def set_delay_state(self, state):
        self._device.auto_delay_on = self.bool_onoff_value(state)

    def set_init_state(self, state):
        self._device.init_state_on = self.bool_onoff_value(state)

    def get_init_state(self):
        return self.enum_onoff_value(self._device.init_state_on)

    def set_sample_count(self, count):
        self._device.sample_count = count

    def get_sample_count(self):
        return "{0}".format(self._device.sample_count)

    def set_source(self, source):
        if source in CONTROL_SOURCE.values():
            self._device.source = CONTROL_SOURCE.keys()[CONTROL_SOURCE.values().index(source)]
        else:
            raise ValueError("Invalid control source value")

    def set_data_elements(self):
        self._device.data_elements = "READ, CHAN, TST"

    def set_auto_range_status(self, state):
        self._device.auto_range_on = self.bool_onoff_value(state)

    def get_auto_range_status(self):
        return self.enum_onoff_value(self._device.auto_range_on)

    def set_resistance_digits(self, digit, start, end):
        self._device.measurement_digits = digit

    def set_resistance_rate(self, rate):
        self._device.nplc = rate

    def set_scan_state(self, state):
        if state in SCAN_STATE.values():
            self._device.scan_state_status = SCAN_STATE.keys()[SCAN_STATE.values().index(state)]
        else:
            raise ValueError("Invalid scan state source value")

    def get_scan_state(self):
        return SCAN_STATE[self._device.scan_state_status]

    def get_scan_channels(self):
        return "(@{}:110,201:{})".format(self._device.scan_channel_start, self._device.scan_channel_end)

    def set_scan_channels(self, start, end):
        self._device.scan_channel_start = start
        self._device.scan_channel_end = end