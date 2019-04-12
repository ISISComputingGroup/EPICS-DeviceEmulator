import traceback

from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log

MEASUREMENT_TYPE = {0: "VOLT:DC", 1: "VOLT:AC", 2: "CURR:DC", 3: "CURR:AC", 4: "RES", 5: "FRES", 6: "CONT",
                    7: "FREQ", 8: "PER"}
BUFFER_SOURCE = {0: "SENS", 1: "CALC", 2: "NONE"}
BUFFER_CONTROL_MODE = {0: "NEXT", 1: "ALW", 2: "NEV"}
TIMESTAMP_FORMAT = {0: "ABS", 1: "DELT"}
CONTROL_SOURCE = {0: "IMM", 1: "TIM", 2: "MAN", 3: "BUS", 4: "EXT"}
SCAN_STATE = {0: "INT", 1: "NONE"}


@has_log
class Keithley2700StreamInterface(StreamInterface):
    in_terminator = "\r"
    out_terminator = "\r"
    commands = {
        # get_multicmds splits commands by ';' if multiple command strings are received
        CmdBuilder("get_multicmds", arg_sep="", ignore_case=True).get_multicommands(";")
                                                                 .build(),

        # Extra split on newline to make compatible with VI
        CmdBuilder("get_multicmds", arg_sep="", ignore_case=True).get_multicommands("\n")
                                                                 .build(),

        CmdBuilder("get_idn", ignore_case=True).escape("*IDN?")
                                               .eos().build(),

        CmdBuilder("empty_queue", ignore_case=True).escape(":SYST:CLE")
                                                   .eos().build(),

        CmdBuilder("clear_buffer", ignore_case=True).escape("TRAC:CLE")
                                                    .eos().build(),

        CmdBuilder("set_measurement", ignore_case=True).escape(":FUNC ")
                                                       .regex("(?:\'|\")")
                                                       .arg("VOLT:DC|VOLT:AC|CURR:DC|CURR:AC|RES|FRES|CONT|FREQ|PER")
                                                       .spaces(at_least_one=False).regex("(?:\'|\")")
                                                       .spaces(at_least_one=False).escape(",")
                                                       .spaces(at_least_one=False).escape("(@101:210)")
                                                       .eos().build(),

        CmdBuilder("get_measurement", ignore_case=True).escape(":FUNC?")
                                                       .eos().build(),

        CmdBuilder("set_buffer_feed", ignore_case=True).escape("TRAC:FEED ")
                                                       .arg("SENS|CALC|NONE")
                                                       .eos().build(),

        CmdBuilder("set_buffer_control", ignore_case=True).escape("TRAC:FEED:CONT ")
                                                          .arg("NEV|NEXT|ALW")
                                                          .eos().build(),

        CmdBuilder("set_buffer_state", ignore_case=True).escape("TRAC:CLE:AUTO ")
                                                        .arg("OFF|ON")
                                                        .eos().build(),

        CmdBuilder("get_buffer_state", ignore_case=True).escape("TRAC:CLE:AUTO?")
                                                        .eos().build(),

        CmdBuilder("get_next_buffer_location", ignore_case=True).escape("TRAC:NEXT?")
                                                                .eos().build(),

        CmdBuilder("get_buffer_stats", ignore_case=True).escape("TRAC:FREE?")
                                                        .eos().build(),

        CmdBuilder("get_readings",  arg_sep="", ignore_case=True).escape("TRAC:DATA:SEL? ")
                                                                 .int().escape(",").int()
                                                                 .eos().build(),

        CmdBuilder("set_buffer_size", ignore_case=True).escape("TRAC:POIN ")
                                                       .int()
                                                       .eos().build(),

        CmdBuilder("get_buffer_size", ignore_case=True).escape("TRAC:POIN?")
                                                       .eos().build(),

        CmdBuilder("set_time_stamp_format", ignore_case=True).escape("TRAC:TST:FORM ")
                                                             .arg("ABS|DELT")
                                                             .eos().build(),

        CmdBuilder("get_time_stamp_format", ignore_case=True).escape("TRAC:TST:FORM?")
                                                             .eos().build(),

        CmdBuilder("get_delay_state", ignore_case=True).escape("TRIG:DEL:AUTO?")
                                                       .eos().build(),

        CmdBuilder("set_delay_state", ignore_case=True).escape("TRIG:DEL:AUTO ")
                                                       .arg("OFF|ON")
                                                       .eos().build(),

        CmdBuilder("set_init_state", ignore_case=True).escape("INIT:CONT ")
                                                      .arg("OFF|ON")
                                                      .eos().build(),

        CmdBuilder("get_init_state", ignore_case=True).escape("INIT:CONT?")
                                                      .eos().build(),

        CmdBuilder("set_sample_count", ignore_case=True).escape("SAMP:COUN ")
                                                        .int()
                                                        .eos().build(),

        CmdBuilder("get_sample_count", ignore_case=True).escape("SAMP:COUN?")
                                                        .eos().build(),

        CmdBuilder("set_source", ignore_case=True).escape("TRIG:SOUR ")
                                                  .arg("IMM|TIM|MAN|BUS|EXT")
                                                  .eos().build(),

        CmdBuilder("set_data_elements", ignore_case=True).escape("FORM:ELEM READ,")
                                                         .spaces(at_least_one=False)
                                                         .escape("CHAN,").spaces(at_least_one=False)
                                                         .escape("TST").spaces(at_least_one=False)
                                                         .eos().build(),

        CmdBuilder("set_auto_range_status", arg_sep="", ignore_case=True).optional(":").escape("FRES:RANG:AUTO ")
                                                                         .arg("OFF|ON").spaces(at_least_one=False)
                                                                         .optional(",").spaces(at_least_one=False)
                                                                         .optional("(@101:210)")
                                                                         .eos().build(),

        CmdBuilder("get_auto_range_status", ignore_case=True).optional(":").escape("FRES:RANG:AUTO?")
                                                             .eos().build(),

        CmdBuilder("set_resistance_digits", arg_sep="", ignore_case=True).optional(";").escape(":FRES:DIG ")
                                                                         .int().spaces(at_least_one=False)
                                                                         .escape(", (@")
                                                                         .int().escape(":").int()
                                                                         .escape(")")
                                                                         .eos().build(),

        CmdBuilder("set_resistance_rate", ignore_case=True).optional(";").escape(":FRES:NPLC ")
                                                           .float().optional("E+0")
                                                           .eos().build(),

        CmdBuilder("set_scan_state", ignore_case=True).escape("ROUT:SCAN:LSEL ")
                                                      .arg("INT|NONE")
                                                      .eos().build(),

        CmdBuilder("get_scan_state", ignore_case=True).escape("ROUT:SCAN:LSEL?")
                                                      .eos().build(),

        CmdBuilder("set_scan_channels", arg_sep="", ignore_case=True).escape("ROUT:SCAN (@")
                                                                     .int().escape(":").int()
                                                                     .escape(")")
                                                                     .eos().build(),

        CmdBuilder("get_scan_channels", ignore_case=True).escape("ROUT:SCAN?")
                                                         .eos().build(),
    }

    def handle_error(self, request, error):
        self.log.error("An error occurred at request" + repr(request) + ": " + repr(error))
        self.log.error(traceback.format_exc())
        print("An error occurred at request '" + repr(request) + "': '" + repr(error) + "'")

    def bool_onoff_value(self, string_value):
        if string_value not in ["ON", "OFF"]:
            raise ValueError("Invalid on/off value!")
        return string_value == "ON"

    def enum_onoff_value(self, bool_value):
        if bool_value not in [True, False]:
            raise ValueError("Invalid on/off value!")
        else:
            return int(bool_value)

    def get_idn(self):
        return self._device.idn

    def empty_queue(self):
        self.log.info("Error log emptied")

    def clear_buffer(self):
        self._device.clear_buffer()

    def set_measurement(self, measurement):
        if measurement in MEASUREMENT_TYPE.values():
            self._device.measurement = MEASUREMENT_TYPE.keys()[MEASUREMENT_TYPE.values().index(measurement)]
        else:
            raise ValueError("Invalid measurement value!")

    def get_measurement(self):
        return "\"{}\"".format(MEASUREMENT_TYPE[self._device.measurement])

    def set_buffer_feed(self, feed):
        if feed in BUFFER_SOURCE.values():
            self._device.buffer_feed = BUFFER_SOURCE.keys()[BUFFER_SOURCE.values().index(feed)]
        else:
            raise ValueError("Invalid feed source value!")

    def set_buffer_control(self, control):
        if control in BUFFER_CONTROL_MODE.values():
            self._device.buffer_control = BUFFER_CONTROL_MODE.keys()[BUFFER_CONTROL_MODE.values().index(control)]
        else:
            raise ValueError("Invalid buffer control source value!")

    def set_buffer_state(self, state):
        self._device.buffer_autoclear_on = state

    def get_buffer_state(self):
        return "{}".format("1" if self._device.buffer_autoclear_on else "0")

    def get_next_buffer_location(self):
        """
        :return: String-formatted integer of the next buffer location to retrieve
        """
        next_location = self._device.get_next_buffer_location()
        self.log.info("Next buffer location: {}".format(next_location))
        return "{}".format(next_location)

    def get_buffer_stats(self):
        """
        :return: String containing number of bytes available, and number of bytes used
        """
        return "{}, {}".format(str(self._device.bytes_available), str(self._device.bytes_used))

    def get_readings(self, start, count):
        """
        :param start: Start location in buffer
        :param count:number of readings to retrieve
        :return: String value of readings from buffer
        """

        chunks = []
        start, count = int(start), int(count)
        for buffer_location in range(start, start + count):
            chunks.append("{},{},{}".format(self._device.buffer[buffer_location].reading,
                                            self._device.buffer[buffer_location].timestamp,
                                            self._device.buffer[buffer_location].channel))

        self.log.info("Returned readings: {}".format("No readings" if (len(chunks) == 0) else ",".join(chunks)))
        return ", ".join(chunks)

    def set_buffer_size(self, size):
        self._device.buffer_size = int(size)

    def get_buffer_size(self):
        return self._device.buffer_size

    def set_time_stamp_format(self, timestamp_format):
        if timestamp_format in TIMESTAMP_FORMAT.values():
            self._device.time_stamp_format = TIMESTAMP_FORMAT.keys()[TIMESTAMP_FORMAT.values().index(timestamp_format)]
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
            self._device.scan_channel_start = start
            self._device.scan_channel_end = end

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

    def get_multicmds(self, command, other_commands):
        """
             Added specifically to support use of the VI with the emulator, as the VI sends multiple commands
             in one go, separated by semicolons.
        """
        replies = []
        for cmd_to_find in [command, other_commands]:
            if cmd_to_find != "":
                self.log.info("Processing {} from combined command".format(cmd_to_find))
                reply = self._process_part_command(cmd_to_find)
                if reply is not None:
                    replies.append(self._process_part_command(cmd_to_find))
        return self.out_terminator.join(replies)

    def _process_part_command(self, cmd_to_find):
        for cmd in self.bound_commands:
            if cmd.can_process(cmd_to_find):
                return cmd.process_request(cmd_to_find)
        self.log.info("Error, unable to find command: '{}'".format(cmd_to_find))
