import re

from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder

@has_log
class Lakeshore460StreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    commands = {
        # Split commands by ';' if multiple command strings are received
        CmdBuilder("get_multicmds", arg_sep="").arg("[^;]+").escape(";").arg(".*").build(),

        CmdBuilder("get_IDN").escape("*IDN?").build(),
        CmdBuilder("get_source").escape("VSRC?").build(),
        CmdBuilder("set_source").escape("VSRC ").digit().build(),
        CmdBuilder("get_channel").escape("CHNL?").build(),
        CmdBuilder("set_channel").escape("CHNL ").arg("X|Y|Z|V").endOfString().build(),

        CmdBuilder("get_magnetic_field_reading").escape("FIELD?").build(),
        CmdBuilder("get_magnetic_field_reading_multiplier").escape("FIELDM?").build(),
        CmdBuilder("get_max_hold_reading").escape("MAXR?").build(),
        CmdBuilder("get_max_hold_reading_multiplier").escape("MAXRM?").build(),
        CmdBuilder("get_relative_mode_reading").escape("RELR?").build(),
        CmdBuilder("get_relative_mode_multiplier").escape("RELRM?").build(),
        CmdBuilder("get_unit").escape("UNIT?").build(),
        CmdBuilder("set_unit").escape("UNIT ").arg("G|T").build(),
        CmdBuilder("get_ac_dc_mode").escape("ACDC?").build(),
        CmdBuilder("set_ac_dc_mode").escape("ACDC ").arg("0|1").build(),
        CmdBuilder("get_prms_reading").escape("PRMS?").build(),
        CmdBuilder("set_prms_reading").escape("PRMS ").arg("0|1").build(),
        CmdBuilder("set_filter_status").escape("FILT ").arg("0|1").build(),
        CmdBuilder("get_filter_status").escape("FILT?").build(),
        CmdBuilder("set_relative_mode_status").escape("REL ").arg("0|1").build(),
        CmdBuilder("get_relative_mode_status").escape("REL?").build(),
        CmdBuilder("get_relative_setpoint").escape("RELS?").build(),
        CmdBuilder("set_relative_setpoint").escape("REL ").float().build(),
        CmdBuilder("get_relative_setpoint_multiplier").escape("RELSM?").build(),
        CmdBuilder("set_auto_mode_status").escape("AUTO ").arg("0|1").build(),
        CmdBuilder("get_auto_mode_status").escape("AUTO?").build(),
        CmdBuilder("set_max_hold_status").escape("MAX ").arg("0|1").build(),
        CmdBuilder("get_max_hold_status").escape("MAX?").build(),
        CmdBuilder("get_channel_status").escape("ONOFF?").build(),
        CmdBuilder("set_channel_status").escape("ONOFF ").arg("0|1").build(),
        CmdBuilder("get_filter_windows").escape("FWIN?").build(),
        CmdBuilder("set_filter_windows").escape("FWIN ").int().build(),
        CmdBuilder("set_filter_points").escape("FNUM ").int().build(),
        CmdBuilder("get_filter_points").escape("FNUM?").build(),
        CmdBuilder("get_manual_range").escape("RANGE?").build(),
        CmdBuilder("set_manual_range").escape("RANGE ").int().build(),
    }

    def update_reading(self, reading, multiplier):
        """
        :param reading: A reading from the device
        :param multiplier: The current multiplier for the reading
        :return:    new_reading: updated reading value, based on more appropriate multiplier
                    new_multiplier: updated multiplier for the value
        """
        stripped_reading = self.strip_multiplier(reading, multiplier)
        new_multiplier = self.calculate_multiplier(stripped_reading)
        new_reading = self.apply_multiplier(stripped_reading, new_multiplier)
        return new_reading, new_multiplier

    def strip_multiplier(self, reading, multiplier):
        """
        :param reading:  A reading from the device with multiplier applied
        :param multiplier: The current multiplier for the reading
        :return: The raw reading
        """
        if multiplier == "u":
            return reading * 0.000001
        if multiplier == "m":
            return reading * 0.001
        if multiplier == "k":
            return reading * 1000
        else:
            return reading

    def apply_multiplier(self, reading, multiplier):
        """
        :param reading: A raw reading from the device
        :param multiplier: The multiplier to be applied
        :return: The reading with the multiplier applied
        """
        if multiplier == "u":
            return reading / 0.000001
        if multiplier == "m":
            return reading / 0.001
        if multiplier == "k":
            return reading / 1000
        else:
            return reading

    def convert_units(self, convert_value):
        """
        Converts between Tesla and Gauss (applies conversion of *10000 or *0.0001)
        Then updates reading values according to more appropriate multiplier
        :param convert_value: 10000 or 0.0001
        """
        channels = ['X', 'Y', 'Z', 'V']
        for c in channels:
            self.set_channel(c)
            self._device.channels[c].field_reading *= convert_value
            self._device.channels[c].field_reading, \
            self._device.channels[c].field_multiplier = self.update_reading(self._device.channels[c].field_reading,
                                                                            self._device.channels[c].field_multiplier)
            self._device.channels[c].max_hold_reading *= convert_value
            self._device.channels[c].max_hold_reading, \
            self._device.channels[c].max_hold_multiplier = self.update_reading(self._device.channels[c].max_hold_reading,
                                                                                self._device.channels[c].max_hold_multiplier)
            self._device.channels[c].rel_mode_reading *= convert_value
            self._device.channels[c].rel_mode_reading, \
            self._device.channels[c].rel_mode_multiplier = self.update_reading(self._device.channels[c].rel_mode_reading,
                                                                                self._device.channels[c].rel_mode_multiplier)
            self._device.channels[c].relative_setpoint *= convert_value
            self._device.channels[c].relative_setpoint, \
            self._device.channels[c].relative_setpoint_multiplier = self.update_reading(self._device.channels[c].relative_setpoint,
                                                                                self._device.channels[c].relative_setpoint_multiplier)


    def calculate_multiplier(self, reading):
        """
        Calculates the most appropriate multiplier for a given value.
        :param reading: A raw reading from the device
        :return: The most appropriate multiplier value for the given raw reading
        """
        if reading < 0.001:
            return "u"
        if reading >= 0.001 and reading < 0:
            return "m"
        if reading > 0 and reading < 1000:
            return " "
        else:
            return "k"

    def update_reading(self, reading, multiplier):
        stripped_reading = self.strip_multiplier(reading, multiplier)
        new_multiplier = self.calculate_multiplier(stripped_reading)
        new_reading = self.apply_multiplier(stripped_reading, new_multiplier)
        return new_reading, new_multiplier

    def handle_error(self, request, error):
        self.log.error("An error occurred at request" + repr(request) + ": " + repr(error))
        print("An error occurred at request" + repr(request) + ": " + repr(error))

    def get_IDN(self):
        return "{0}".format(self._device.idn)

    def set_source(self, source):
        self._device.source = source

    def get_source(self):
        return "{0}".format(self._device.source)

    def set_channel(self, channel):
        self._device.channel = channel

    def get_channel(self):
        return self._device.channel

    def get_magnetic_field_reading(self):
        field_reading = self._device.channels[self.get_channel()].field_reading
        multiplier = self._device.channels[self.get_channel()].field_multiplier

        # Update max_hold_reading if field_reading is larger
        if field_reading > self._device.channels[self.get_channel()].max_hold_reading:
            self._device.channels[self.get_channel()].max_hold_reading = field_reading
            self._device.channels[self.get_channel()].max_hold_reading_multiplier = multiplier

        return "{0}".format(self._device.channels[self.get_channel()].field_reading)

    def get_magnetic_field_reading_multiplier(self):
        return "{0}".format(self._device.channels[self.get_channel()].field_multiplier)

    def get_max_hold_reading(self):
        return "{0}".format(self._device.channels[self.get_channel()].max_hold_reading)

    def get_max_hold_reading_multiplier(self):
        return "{0}".format(self._device.channels[self.get_channel()].max_hold_multiplier)

    def get_relative_mode_reading(self):
        return "{0}".format(self._device.channels[self.get_channel()].rel_mode_reading)

    def get_relative_mode_multiplier(self):
        return "{0}".format(self._device.channels[self.get_channel()].rel_mode_multiplier)

    def get_unit(self):
        return "{0}".format(self._device.unit)

    def set_unit(self, unit):
        # Convert values if required
        if self._device.unit == "T":
            if unit == "G":
                self.convert_units(10000)
        if self._device.unit == "G":
            if unit == "T":
                self.convert_units(0.0001)
        self._device.unit = unit

    def get_ac_dc_mode(self):
        return "{0}".format(self._device.channels[self.get_channel()].mode)

    def set_ac_dc_mode(self, mode):
        self._device.channels[self.get_channel()].mode = mode

    def get_prms_reading(self):
        return "{0}".format(self._device.channels[self.get_channel()].prms)

    def set_prms_reading(self, prms):
        self._device.channels[self.get_channel()].prms = prms

    def get_filter_status(self):
        return "{0}".format(self._device.channels[self.get_channel()].filter_status)

    def set_filter_status(self, filter):
        self._device.channels[self.get_channel()].filter_status = filter

    def set_relative_mode_status(self, rel_mode):
        self._device.channels[self.get_channel()].rel_mode_status = rel_mode

    def get_relative_mode_status(self):
        return "{0}".format(self._device.channels[self.get_channel()].rel_mode_status)

    def set_auto_mode_status(self, auto_mode_status):
        self._device.channels[self.get_channel()].auto_mode_status = auto_mode_status

    def get_auto_mode_status(self):
        return "{0}".format(self._device.channels[self.get_channel()].auto_mode_status)

    def set_max_hold_status(self, max_hold_status):
        self._device.channels[self.get_channel()].max_hold_status = max_hold_status

    def get_max_hold_status(self):
        return "{0}".format(self._device.channels[self.get_channel()].max_hold_status)

    def get_channel_status(self):
        return "{0}".format(self._device.channels[self.get_channel()].channel_status)

    def set_channel_status(self, status):
        self._device.channels[self.get_channel()].channel_status = status

    def get_filter_windows(self):
        return "{0}".format(self._device.channels[self._device.channel].filter_windows)

    def set_filter_windows(self, percentage):
        self._device.channels[self.get_channel()].filter_windows = percentage

    def get_filter_points(self):
        return "{0}".format(self._device.channels[self.get_channel()].filter_points)

    def set_filter_points(self, points):
        self._device.channels[self.get_channel()].filter_points = points

    def set_manual_range(self, range):
        self._device.channels[self.get_channel()].manual_range = range

    def get_manual_range(self):
        return "{0}".format(self._device.channels[self.get_channel()].manual_range)

    def get_relative_setpoint(self):
        return self._device.channels[self.get_channel()].relative_setpoint

    def set_relative_setpoint(self, rel_setpoint):
        self._device.channels[self.get_channel()].relative_setpoint = rel_setpoint

    def get_relative_setpoint_multiplier(self):
        return self._device.channels[self.get_channel()].relative_setpoint_multiplier

    # As the protocol file sends multiple commands (set Channel; request channel PV),
    # these methods split up the commands and process both.

    def get_multicmds(self, command, other_commands):
        replies = []
        for cmd_to_find in [command, other_commands]:
            self.log.info("cmd {}".format(cmd_to_find))
            reply = self._process_part_command(cmd_to_find)
            if reply is not None:
                replies.append(self._process_part_command(cmd_to_find))
        return self.out_terminator.join(replies)

    def _process_part_command(self, cmd_to_find):
        for cmd in self.bound_commands:
            if cmd.can_process(cmd_to_find):
                return cmd.process_request(cmd_to_find)
