from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")

ISOBUS_PREFIX = "@1"


@has_log
class MercuryitcInterface(StreamInterface):
    commands = {
        CmdBuilder("get_catalog").optional(ISOBUS_PREFIX)
            .escape("READ:SYS:CAT").eos().build(),
        CmdBuilder("get_nickname").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":").any().escape(":NICK").eos().build(),
        CmdBuilder("read_calib_tables").optional(ISOBUS_PREFIX)
            .escape("READ:FILE:calibration_tables:LIST").eos().build(),

        CmdBuilder("get_all_temp_sensor_details").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP").eos().build(),
        CmdBuilder("get_all_heater_details").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":HTR").eos().build(),
        CmdBuilder("get_all_aux_details").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":AUX").eos().build(),

        CmdBuilder("get_temp_p").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:P").eos().build(),
        CmdBuilder("get_temp_i").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:I").eos().build(),
        CmdBuilder("get_temp_d").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:D").eos().build(),
        CmdBuilder("get_temp_measured").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:SIG:TEMP").eos().build(),
        CmdBuilder("get_temp_setpoint").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:TSET").eos().build(),


    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)

        return "{}:INVALID".format(request.lstrip(ISOBUS_PREFIX))

    @if_connected
    def get_catalog(self):
        resp = "STAT:SYS:CAT"

        for chan_location, chan in self.device.channels.items():
            resp += ":DEV:{}:{}".format(chan_location, chan.channel_type)

        return resp

    def _chan_from_id(self, deviceid, expected_type=None):
        if deviceid not in self.device.channels.keys():
            msg = "Unknown channel {}".format(deviceid)
            self.log.error(msg)
            raise ValueError(msg)

        if expected_type is not None and self.device.channels[deviceid].channel_type != expected_type:
            msg = "Unexpected channel type for {} (expected {}, was {})"\
                .format(deviceid, expected_type, self.device.channels[deviceid].channel_type)
            self.log.error(msg)
            raise ValueError(msg)

        return self.device.channels[deviceid]

    @if_connected
    def get_nickname(self, deviceid, _):
        chan = self._chan_from_id(deviceid)
        return "STAT:DEV:{}:NICK:{}".format(deviceid, chan.nickname)

    @if_connected
    def read_calib_tables(self):
        """ This is only required to prevent an error from the labview driver. """
        return ""

    @if_connected
    def get_all_temp_sensor_details(self, deviceid):
        """
        Gets the details for an entire temperature sensor all at once. This is only used by the LabVIEW VI, not by
        the IOC (the ioc queries each parameter individually)
        """

        chan = self._chan_from_id(deviceid)

        return "STAT:DEV:{}:TEMP:".format(deviceid) + \
               ":NICK:{}".format(chan.nickname) + \
               ":LOOP" + \
                 ":AUX:{}".format(chan.associated_aux_channel) + \
                 ":D:{}".format(chan.d) + \
                 ":HTR:{}".format(chan.associated_heater_channel) + \
                 ":I:{}".format(chan.i) + \
                 ":HSET:{}".format(chan.heater_percent) + \
                 ":PIDT:{}".format("ON" if chan.autopid else "OFF") + \
                 ":ENAB:{}".format("ON" if chan.heater_auto else "OFF") + \
                 ":FAUT:{}".format("ON" if chan.gas_flow_auto else "OFF") + \
                 ":FSET:{}".format(chan.gas_flow) + \
                 ":PIDF:{}".format(chan.autopid_file if chan.autopid else "None") + \
                 ":P:{}".format(chan.p) + \
                 ":TSET:{:.4f}K".format(chan.temperature_sp) + \
               ":CAL" + \
                 ":FILE:{}".format(chan.calibration_file) + \
               ":SIG" + \
                 ":TEMP:{:.4f}K".format(chan.temperature) + \
                 ":RES:{:.4f}O".format(chan.resistance)

    @if_connected
    def get_temp_p(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:P:{}".format(deviceid, chan.p)

    @if_connected
    def get_temp_i(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:I:{}".format(deviceid, chan.i)

    @if_connected
    def get_temp_d(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:D:{}".format(deviceid, chan.d)

    @if_connected
    def get_temp_measured(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:SIG:TEMP:{:.4f}K".format(deviceid, chan.temperature)

    @if_connected
    def get_temp_setpoint(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:TSET:{:.4f}K".format(deviceid, chan.temperature_sp)

    @if_connected
    def get_all_heater_details(self, deviceid):
        """
        Gets the details for an entire heater sensor all at once. This is only used by the LabVIEW VI, not by
        the IOC (the ioc queries each parameter individually)
        """

        chan = self._chan_from_id(deviceid)

        return "STAT:DEV:{}:HTR".format(deviceid) + \
               ":NICK:{}".format(chan.nickname) + \
               ":VLIM:{}".format(chan.voltage_limit) + \
               ":SIG" + \
                 ":VOLT:{:.4f}V".format(chan.voltage) + \
                 ":CURR:{:.4f}A".format(chan.current) + \
                 ":POWR:{:.4f}W".format(chan.power)

    @if_connected
    def get_all_aux_details(self, deviceid):
        """
        Gets the details for an entire aux sensor all at once. This is only used by the LabVIEW VI, not by
        the IOC (the ioc queries each parameter individually)
        """
        chan = self._chan_from_id(deviceid)

        return "STAT:DEV:{}:AUX".format(deviceid) + \
               ":NICK:{}".format(chan.nickname) + \
               ":SIG" \
                 ":PERC:{:.4f}".format(chan.percent_open)
