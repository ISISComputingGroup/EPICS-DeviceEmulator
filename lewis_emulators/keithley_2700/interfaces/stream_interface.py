from lewis.adapters.stream import StreamInterface, StreamAdapter
from utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
import random


@has_log
class Keithley2700StreamInterface(StreamInterface):
    in_terminator = "\r\n"
    out_terminator = "\r\n"
    commands = {
        CmdBuilder("get_idn").escape("*IDN?").build(),
        CmdBuilder("empty_queue").escape("SYST:CLE").build(),
        CmdBuilder("clear_buffer").escape("TRAC:CLE").build(),
        CmdBuilder("set_measurement").escape(":FUNC ").arg("VOLT|VOLT:AC|CURR|CURR:AC|RES|FRES|CONT|FREQ|PER").build(),
        CmdBuilder("set_buffer_feed").escape("TRAC:FEED ").arg("SENS|CALC|NONE").build(),
        CmdBuilder("set_buffer_control").escape("TRAC:FEED:CONT ").arg("NEV|NEXT|ALW").build(),
        CmdBuilder("set_buffer_state").escape("TRAC:CLE:AUTO ").arg("ON|OFF").build(),
        CmdBuilder("get_next_buffer_location").escape("TRAC:NEXT?").build(),
        CmdBuilder("get_buffer_stats").escape("TRAC:FREE?").build(),
        CmdBuilder("get_readings_range",  arg_sep="").escape("TRAC:DATA:SEL? ").int().escape(",").int().build(),
        CmdBuilder("set_buffer_size").escape("TRAC:POIN ").int().build(),
        CmdBuilder("set_time_stamp_format").escape("TRAC:TST:FORM ").arg("ABS|DELT").build(),
        CmdBuilder("get_delay_state").escape("TRIG:DEL:AUTO?").build(),
        CmdBuilder("set_delay_state").escape("TRIG:DEL:AUTO ").arg("ON|OFF").build(),
        CmdBuilder("set_init_state").escape("INIT:CONT ").arg("ON|OFF").build(),
        CmdBuilder("get_init_state").escape("INIT:CONT?").build(),
        CmdBuilder("set_sample_count").escape("SAMP:COUN ").int().build(),
        CmdBuilder("get_sample_count").escape("SAMP:COUN?").build(),
        CmdBuilder("set_source").escape("TRIG:SOUR ").arg("IMM|TIM|MAN|BUS|EXT").build(),
        CmdBuilder("set_data_elements").escape("FORM:ELEM READ, CHAN, TST").build(),
        CmdBuilder("set_auto_range_status", arg_sep="").escape("FRES:RANG:AUTO ").arg("ON|OFF").
        escape(", (@").int().escape(":").int().escape(")").build(),
        CmdBuilder("set_resistance_digits", arg_sep="").escape(":FRES:DIG ").int().escape(", (@").
        int().escape(":").int().escape(")").build(),
        CmdBuilder("set_resistance_rate").escape(":FRES:NPLC ").float().build(),
        CmdBuilder("set_scan_state").escape("ROUT:SCAN:LSEL ").arg("NONE|INT").build(),
        CmdBuilder("set_scan_channels", arg_sep="").escape("ROUT:SCAN (@").int().escape(":").int().escape(")").build(),
        CmdBuilder("get_scan_channels").escape("ROUT:SCAN?").build()
    }

    def handle_error(self, request, error):
        self.log.error("An error occurred at request" + repr(request) + ": " + repr(error))
        print("An error occurred at request" + repr(request) + ": " + repr(error))

    def check_valid_channel_value(self, channel, device_value):
        if int(channel) != int(device_value):
            raise ValueError("Unexpected channel value: expected {}, got {}".format(device_value, channel))
        else:
            return True

    def get_idn(self):
        """
        Replies with the device's identity.
        """
        return "{}".format(self._device.idn)

    def empty_queue(self):
        self.log.info("Error log emptied")

    def clear_buffer(self):
        self._device.buffer = ""

    def set_measurement(self, measurement):
        self._device.measurement = measurement

    def set_buffer_feed(self, feed):
        self._device.buffer_feed = feed

    def set_buffer_control(self, control):
        self._device.buffer_control = control

    def set_buffer_state(self, state):
        self._device.buffer_state = state

    def get_next_buffer_location(self):
        count = random.randint(2, 8)
        self._device.next_buffer_location = self._device.current_buffer_loc + count
        # If the next buffer location is larger than the buffer size, restart from the beginning of the buffer
        if self._device.next_buffer_location >= len(self._device.buffer_full):
            self._device.next_buffer_location -= len(self._device.buffer_full)
            self._device.current_buffer_loc = 0

        return "{}".format(self._device.next_buffer_location)

    def get_buffer_stats(self):
        return "{}, {}".format(str(self._device.bytes_available), str(self._device.bytes_used))

    def get_readings_range(self, start, count):
        # Return channel readings from location to + count
        self._device.buffer_range_readings = ""
        for i in xrange(int(count)):
            if int(self._device.current_buffer_loc) >= len(self._device.buffer_full):
                self._device.next_buffer_location = len(self._device.buffer_full) - self._device.current_buffer_loc + i
                self._device.current_buffer_loc = 0
                self._device.fill_buffer()
            else:
                next_reading = str(self._device.buffer_full[int(self._device.current_buffer_loc)])
                self._device.current_buffer_loc += 1
                self._device.buffer_range_readings += next_reading
        #self.log.info("\n\n>> READINGS: {}\n".format(self._device.buffer_range_readings))

        return self._device.buffer_range_readings

    def set_buffer_size(self, size):
        self._device.buffer_size = size

    def set_time_stamp_format(self, format):
        self._device.time_stamp_format = format

    def get_delay_state(self):
        return "{0}".format(self._device.delay_state)

    def set_delay_state(self, state):
        self._device.delay_state = state

    def set_init_state(self, state):
        self._device.init_state = state

    def get_init_state(self):
        return "{0}".format(self._device.init_state)

    def set_sample_count(self, count):
        self._device.sample_count = count

    def get_sample_count(self):
        return "{0}".format(self._device.sample_count)

    def set_source(self, source):
        self._device.source = source

    def set_data_elements(self):
        self._device.data_elements = "READ, CHAN, TST"

    def set_auto_range_status(self, state, start, end):
        self._device.auto_range_status = state

    def set_resistance_digits(self, digit, start, end):
            self._device.measurement_digits = digit

    def set_resistance_rate(self, rate):
        self._device.nplc = rate

    def set_scan_state(self, state):
        self._device.scan_state_status = state

    def get_scan_channels(self):
        return "(@{}:{})".format(self._device.scan_channel_start, self._device.scan_channel_end)

    def set_scan_channels(self, start, end):
        self._device.scan_channel_start = start
        self._device.scan_channel_end = end
