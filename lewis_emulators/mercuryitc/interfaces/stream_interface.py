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
            .escape("READ:DEV:").any().escape(":NICK").eos().build(),

        CmdBuilder("get_all_temp_sensor_details").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any().escape(":TEMP").eos().build(),
        CmdBuilder("get_all_heater_details").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any().escape(":HTR").eos().build(),
        CmdBuilder("get_all_aux_details").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any().escape(":AUX").eos().build(),
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    @if_connected
    def get_catalog(self):
        resp = "STAT:SYS:CAT"

        for chan_location, chan in self.device.channels.items():
            resp += ":DEV:{}:{}".format(chan_location, chan.channel_type)

        return resp

    @if_connected
    def get_nickname(self, arg):

        deviceid = arg.split(":")[0] if ":" in arg else arg

        if deviceid not in self.device.channels.keys():
            self.log.error("Can't get nickname for ID {}".format(deviceid))
            return "STAT:DEV:{}:NICK:INVALID".format(deviceid)

        return "STAT:DEV:{}:NICK:{}".format(deviceid, self.device.channels[deviceid].nickname)

    @if_connected
    def get_all_temp_sensor_details(self, deviceid):
        """
        Gets the details for an entire temperature sensor all at once. This is only used by the LabVIEW VI, not by
        the IOC (the ioc queries each parameter individually)
        """

        if deviceid not in self.device.channels.keys():
            self.log.error("Can't get all details for ID {} (doesn't exist)".format(deviceid))
            return "STAT:DEV:{}:INVALID".format(deviceid)

        if self.device.channels[deviceid].channel_type != "TEMP":
            self.log.error("Can't get all details for ID {} (incorrect channel type)".format(deviceid))
            return "STAT:DEV:{}:INVALID".format(deviceid)

        chan = self.device.channels[deviceid]

        return "STAT:DEV:{}:TEMP:".format(deviceid) + \
               "EXCT" + \
                 ":TYPE:UNIP" + \
                 ":MAG:0" + \
               ":STAT:40000000" + \
               ":NICK:{}".format(chan.nickname) + \
               ":LOOP" + \
                 ":AUX:{}".format(chan.associated_aux_channel) + \
                 ":D:{}".format(chan.d) + \
                 ":HTR:{}".format(chan.associated_heater_channel) + \
                 ":I:{}".format(chan.i) + \
                 ":THTF:None" + \
                 ":HSET:{}".format(chan.heater_percent) + \
                 ":PIDT:{}".format("ON" if chan.autopid else "OFF") + \
                 ":ENAB:{}".format("ON" if chan.heater_auto else "OFF") + \
                 ":SWFL:None" + \
                 ":FAUT:{}".format("ON" if chan.gas_flow_auto else "OFF") + \
                 ":FSET:{}".format(chan.gas_flow) + \
                 ":PIDF:{}".format(chan.autopid_file if chan.autopid else "None") + \
                 ":P:{}".format(chan.p) + \
                 ":SWMD:FIX" + \
                 ":TSET:{:.4f}K".format(chan.temperature_sp) + \
               ":MAN" + \
                 ":HVER:1" + \
                 ":FVER:1.12" + \
                 ":SERL:111450078" + \
               ":CAL" + \
                 ":OFFS:0" + \
                 ":COLDL:999.00K" + \
                 ":INT:LIN" + \
                 ":SCAL:1" + \
                 ":FILE:{}".format(chan.calibration_file) + \
                 ":HOTL:999.00K" + \
                 ":TYPE:TCE" + \
               ":SIG" + \
                 ":VOLT:-0.0038mV" + \
                 ":CURR:-0.0000A" + \
                 ":TEMP:{:.4f}K".format(chan.temperature) + \
                 ":POWR:0.0000W" + \
                 ":RES:{:.4f}O".format(chan.resistance) + \
                 ":SLOP:0.0000O/K"

    @if_connected
    def get_all_heater_details(self, deviceid):
        """
        Gets the details for an entire heater sensor all at once. This is only used by the LabVIEW VI, not by
        the IOC (the ioc queries each parameter individually)
        """

        if deviceid not in self.device.channels.keys():
            self.log.error("Can't get all details for ID {} (doesn't exist)".format(deviceid))
            return "STAT:DEV:{}:INVALID".format(deviceid)

        if self.device.channels[deviceid].channel_type != "HTR":
            self.log.error("Can't get all details for ID {} (incorrect channel type)".format(deviceid))
            return "STAT:DEV:{}:INVALID".format(deviceid)

        chan = self.device.channels[deviceid]

        return "STAT:DEV:{}:HTR".format(deviceid) + \
               ":STAT:40000000" + \
               ":NICK:{}".format(chan.nickname) + \
               ":PMAX:0.1000" + \
               ":MAN" + \
                 ":HVER:1" + \
                 ":FVER:1.10" + \
                 ":SERL:112123156" + \
               ":TYPE:unknown" + \
               ":VLIM:{}".format(chan.voltage_limit) + \
               ":RES:10" + \
               ":SIG" + \
                 ":VOLT:{:.4f}V".format(chan.voltage) + \
                 ":CURR:{:.4f}A".format(chan.current) + \
                 ":PERC:0.0000%" + \
                 ":POWR:{:.4f}W".format(chan.power)

    @if_connected
    def get_all_aux_details(self, deviceid):

        if deviceid not in self.device.channels.keys():
            self.log.error("Can't get all details for ID {} (doesn't exist)".format(deviceid))
            return "STAT:DEV:{}:INVALID".format(deviceid)

        if self.device.channels[deviceid].channel_type != "AUX":
            self.log.error("Can't get all details for ID {} (incorrect channel type)".format(deviceid))
            return "STAT:DEV:{}:INVALID".format(deviceid)

        chan = self.device.channels[deviceid]

        return "STAT:DEV:{}:AUX".format(deviceid) + \
               ":NICK:{}".format(chan.nickname) + \
               ":SIG" \
                 ":PERC:{:.4f}".format(chan.percent_open)
