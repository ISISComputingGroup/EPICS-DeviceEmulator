from lewis.adapters.stream import StreamAdapter
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log

@has_log
class Lakeshore460StreamInterface(StreamAdapter):

    in_terminator="\r\n"
    out_terminator="\r\n"

    commands = {
        CmdBuilder("get_IDN").escape("*IDN?").build(),
        CmdBuilder("get_unit").escape("UNIT?").build(),
        CmdBuilder("set_unit").escape("UNIT ").arg("G|T").build(),
        CmdBuilder("get_on_off").escape("ONOFF?").build(),
        CmdBuilder("set_on_off").escape("ONOFF ").arg("0|1").build(),
        CmdBuilder("get_ac_dc_field_reading").escape("ACDC?").build(),
        CmdBuilder("set_ac_dc_field_reading").escape("ACDC ").arg("0|1").build(),
        CmdBuilder("get_prms_reading").escape("PRMS?").build(),
        CmdBuilder("set_prms_reading").escape("PRMS ").arg("0|1").build(),
        CmdBuilder("set_display_filter").escape("FILT ").arg("0|1").build(),
        CmdBuilder("get_display_filter").escape("FILT?").build(),
        CmdBuilder("set_max_hold").escape("MAX ").arg("0|1").build(),
        CmdBuilder("get_max_hold").escape("MAX?").build(),
        CmdBuilder("set_auto_range").escape("AUTO ").arg("0|1").build(),
        CmdBuilder("get_auto_range").escape("AUTO?").build(),
        CmdBuilder("set_relative_mode").escape("REL ").arg("0|1").build(),
        CmdBuilder("get_relative_mode").escape("REL?").build(),
        CmdBuilder("get_all_fields").escape("ALLF?").build(),
        CmdBuilder("get_source").escape("VSRC?").build(),
        CmdBuilder("set_source").escape("VSRC ").digit().build(),
        CmdBuilder("get_channel").escape("CHNL?").build(),
        CmdBuilder("set_channel").escape("CHNL ").digit().build(),
        CmdBuilder("get_display_filter_window").escape("FWIN?").build(),
        CmdBuilder("set_display_filter_window").escape("FWIN ").int().build(),
        CmdBuilder("set_filter_points").escape("FNUM ").int().build(),
        CmdBuilder("get_filter_points").escape("FNUM?").build(),
        CmdBuilder("get_manual_range").escape("RANGE?").build(),
        CmdBuilder("set_manual_range").escape("RANGE ").int().build(),
        CmdBuilder("read_relative_mode_set_point_multiplier").escape("RELSM?").build(),
        CmdBuilder("read_relative_mode_set_point").escape("RELS?").build(),
        CmdBuilder("set_relative_mode_set_point").escape("RELS ").float().build(),
        CmdBuilder("read_max_reading").escape("MAXR?").build(),
        CmdBuilder("read_max_reading_multiplier").escape("MAXRM?").build(),
        CmdBuilder("get_relative_mode_reading_multiplier").escape("RELRM?").build(),
        CmdBuilder("get_relative_mode_reading").escape("RELR").build(),
        CmdBuilder("get_magnetic_field_reading_multiplier").escape("FIELDM?").build(),
        CmdBuilder("get_magnetic_field_reading").escape("FIELD?").build()
    }

    def handle_error(self,request, error):
        self.log.error("An error occurred at request {0} : {1} ").format(request, error)
        print("An error occurred at request {0} : {1} ").format(request, error)

    def get_IDN(self):
        return "{0}".format(self._device.idn)

    def get_unit(self):

        return "{0}".format(self._device.unit)

    def set_unit(self, unit):
        self._device.unit = unit

    def get_on_off(self):
        return self._device.status

    def set_on_off(self, status):
        self._device.status = status

    def get_ac_dc_field_reading(self):
        return "{0}".format(self._device.mode)

    def set_ac_dc_field_reading(self, mode):
        self._device.mode = mode

    def get_prms_reading(self):
        return "{0}".format(self._device.prms)

    def set_prms_reading(self, prms):
            self._device.prms = prms

    def get_display_filter(self):
        return "{0}".format(self._device.filter)

    def set_display_filter(self, filter):
            self._device.filter = filter

    def set_max_hold(self, max_hold):
        self._device.max_hold = max_hold

    def get_max_hold(self):
        return "{0}".format(self._device.max_hold)

    def set_relative_mode(self, rel_mode):
        self._device.rel_mode = rel_mode

    def get_relative_mode(self):
        return "{0}".format(self._device.rel_mode)

    def set_auto_range(self, auto_range):
        self._device.auto_range = auto_range

    def get_auto_range(self):
        return "{0}".format(self._device.auto_range)

    def set_manual_range(self, range):
        self._device.manual_range = range

    def get_manual_range(self):
        return "{0}".format(self._device.manual_range)

    def get_all_fields(self):
        return "{0}".format(self._device.total_fields)

    def set_source(self, source):
        self._device.source = source

    def get_source(self):
        return "{0}".format(self._device.source)

    def set_channel(self, channel):
        self._device.channel = channel

    def get_channel(self):
        return "{0}".format(self._device.channel)

    def get_display_filter_window(self):
        return "{0}".format(self._device.display_filter)

    def set_display_filter_window(self, percentage):
        self._device.display_filter = percentage

    def set_filter_points(self, points):
        self._device.filter_points = points

    def get_filter_points(self):
        return "{0}".format(self._device.filter_points)

    def read_relative_mode_set_point_multiplier(self):
        return "{0}".format(self._device.rel_multiplier)

    def read_relative_mode_set_point(self):
        return "{0}".format(self._device.rel_set_point)

    def set_relative_mode_set_point(self, setpoint):
        self._device.rel_set_point = setpoint

    def read_max_reading(self):
        return "{0}".format( self._device.max_reading)

    def read_max_reading_multiplier(self):
        return "{0}".format( self._device.reading_multiplier)

    def get_relative_mode_reading(self):
        return "{0}".format(self._device.rel_mode_reading)

    def get_relative_mode_reading_multiplier(self):
        return "{0}".format(self._device.rel_mode_reading_multiplier)

    def get_magnetic_field_reading(self):
        return "{0}".format(self._device.magnetic_field_reading)

    def get_magnetic_field_reading_multiplier(self):
        return "{0}".format(self._device.magnetic_field_reading_multiplier)
