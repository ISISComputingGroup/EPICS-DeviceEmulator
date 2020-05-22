from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")

ISOBUS_PREFIX = "@1"


@has_log
class MercuryitcInterface(StreamInterface):
    commands = {
        # System-level commands
        CmdBuilder("get_catalog").optional(ISOBUS_PREFIX)
            .escape("READ:SYS:CAT").eos().build(),
        CmdBuilder("read_calib_tables").optional(ISOBUS_PREFIX)
            .escape("READ:FILE:calibration_tables:LIST").eos().build(),
        CmdBuilder("get_nickname").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":").any_except(":").escape(":NICK").eos().build(),
        CmdBuilder("set_nickname").optional(ISOBUS_PREFIX)
            .escape("SET:DEV:").any_except(":").escape(":").any_except(":").escape(":NICK:").any_except(":").eos().build(),

        # Commands to read all info at once
        CmdBuilder("get_all_temp_sensor_details").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP").eos().build(),
        CmdBuilder("get_all_heater_details").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":HTR").eos().build(),
        CmdBuilder("get_all_aux_details").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":AUX").eos().build(),

        # Get heater & aux card associations
        CmdBuilder("get_associated_heater").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:HTR").eos().build(),
        CmdBuilder("get_associated_aux").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:AUX").eos().build(),

        # PID settings
        CmdBuilder("get_autopid").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:PIDT").eos().build(),
        CmdBuilder("set_autopid").optional(ISOBUS_PREFIX)
            .escape("SET:DEV:").any_except(":").escape(":TEMP:LOOP:PIDT:").enum("ON", "OFF").eos().build(),
        CmdBuilder("get_temp_p").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:P").eos().build(),
        CmdBuilder("set_temp_p").optional(ISOBUS_PREFIX)
            .escape("SET:DEV:").any_except(":").escape(":TEMP:LOOP:P:").float().eos().build(),
        CmdBuilder("get_temp_i").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:I").eos().build(),
        CmdBuilder("set_temp_i").optional(ISOBUS_PREFIX)
            .escape("SET:DEV:").any_except(":").escape(":TEMP:LOOP:I:").float().eos().build(),
        CmdBuilder("get_temp_d").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:D").eos().build(),
        CmdBuilder("set_temp_d").optional(ISOBUS_PREFIX)
            .escape("SET:DEV:").any_except(":").escape(":TEMP:LOOP:D:").float().eos().build(),

        # Temperature measurements
        CmdBuilder("get_temp_measured").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:SIG:TEMP").eos().build(),
        CmdBuilder("get_temp_setpoint").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:TSET").eos().build(),
        CmdBuilder("set_temp_setpoint").optional(ISOBUS_PREFIX)
            .escape("SET:DEV:").any_except(":").escape(":TEMP:LOOP:TSET:").float().escape("K").eos().build(),
        CmdBuilder("get_resistance").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:SIG:RES").eos().build(),

        # Heater
        CmdBuilder("get_heater_auto").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:ENAB").eos().build(),
        CmdBuilder("set_heater_auto").optional(ISOBUS_PREFIX)
            .escape("SET:DEV:").any_except(":").escape(":TEMP:LOOP:ENAB:").enum("ON", "OFF").eos().build(),
        CmdBuilder("get_heater_percent").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:HSET").eos().build(),
        CmdBuilder("set_heater_percent").optional(ISOBUS_PREFIX)
            .escape("SET:DEV:").any_except(":").escape(":TEMP:LOOP:HSET:").float().eos().build(),
        CmdBuilder("get_heater_voltage").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":HTR:SIG:VOLT").eos().build(),
        CmdBuilder("get_heater_current").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":HTR:SIG:CURR").eos().build(),
        CmdBuilder("get_heater_power").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":HTR:SIG:POWR").eos().build(),
        CmdBuilder("get_heater_voltage_limit").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":HTR:VLIM").eos().build(),
        CmdBuilder("set_heater_voltage_limit").optional(ISOBUS_PREFIX)
            .escape("SET:DEV:").any_except(":").escape(":HTR:VLIM:").float().eos().build(),

        # Gas flow
        CmdBuilder("get_gas_flow_auto").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":TEMP:LOOP:FAUT").eos().build(),
        CmdBuilder("set_gas_flow_auto").optional(ISOBUS_PREFIX)
            .escape("SET:DEV:").any_except(":").escape(":TEMP:LOOP:FAUT:").enum("ON", "OFF").eos().build(),
        CmdBuilder("get_gas_flow").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any_except(":").escape(":AUX:SIG:PERC").eos().build(),
        CmdBuilder("set_gas_flow").optional(ISOBUS_PREFIX)
            .escape("SET:DEV:").any_except(":").escape(":TEMP:LOOP:FSET:").float().eos().build(),

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
    def get_nickname(self, deviceid, devicetype):
        chan = self._chan_from_id(deviceid, expected_type=devicetype)
        return "STAT:DEV:{}:{}:NICK:{}".format(deviceid, devicetype, chan.nickname)

    @if_connected
    def set_nickname(self, deviceid, devicetype, nickname):
        chan = self._chan_from_id(deviceid, expected_type=devicetype)
        chan.nickname = nickname
        return "STAT:SET:DEV:{}:{}:NICK:{}:VALID".format(deviceid, devicetype, chan.nickname)

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

        temp_chan = self._chan_from_id(deviceid, expected_type="TEMP")
        aux_chan = self._chan_from_id(temp_chan.associated_aux_channel, expected_type="AUX")

        return "STAT:DEV:{}:TEMP:".format(deviceid) + \
               ":NICK:{}".format(temp_chan.nickname) + \
               ":LOOP" + \
                 ":AUX:{}".format(temp_chan.associated_aux_channel) + \
                 ":D:{}".format(temp_chan.d) + \
                 ":HTR:{}".format(temp_chan.associated_heater_channel) + \
                 ":I:{}".format(temp_chan.i) + \
                 ":HSET:{}".format(temp_chan.heater_percent) + \
                 ":PIDT:{}".format("ON" if temp_chan.autopid else "OFF") + \
                 ":ENAB:{}".format("ON" if temp_chan.heater_auto else "OFF") + \
                 ":FAUT:{}".format("ON" if temp_chan.gas_flow_auto else "OFF") + \
                 ":FSET:{}".format(aux_chan.gas_flow) + \
                 ":PIDF:{}".format(temp_chan.autopid_file if temp_chan.autopid else "None") + \
                 ":P:{}".format(temp_chan.p) + \
                 ":TSET:{:.4f}K".format(temp_chan.temperature_sp) + \
               ":CAL" + \
                 ":FILE:{}".format(temp_chan.calibration_file) + \
               ":SIG" + \
                 ":TEMP:{:.4f}K".format(temp_chan.temperature) + \
                 ":RES:{:.4f}O".format(temp_chan.resistance)

    @if_connected
    def get_associated_heater(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:HTR:{}".format(deviceid, chan.associated_heater_channel)

    @if_connected
    def get_associated_aux(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:AUX:{}".format(deviceid, chan.associated_aux_channel)

    @if_connected
    def get_temp_p(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:P:{:.4f}".format(deviceid, chan.p)

    @if_connected
    def set_temp_p(self, deviceid, p):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        chan.p = p
        return "STAT:SET:DEV:{}:TEMP:LOOP:P:{:.4f}:VALID".format(deviceid, p)

    @if_connected
    def get_autopid(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:PIDT:{}".format(deviceid, "ON" if chan.autopid else "OFF")

    @if_connected
    def set_autopid(self, deviceid, sp):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        chan.autopid = (sp == "ON")
        return "STAT:SET:DEV:{}:TEMP:LOOP:PIDT:{}:VALID".format(deviceid, sp)

    @if_connected
    def get_temp_i(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:I:{:.4f}".format(deviceid, chan.i)

    @if_connected
    def set_temp_i(self, deviceid, i):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        chan.i = i
        return "STAT:SET:DEV:{}:TEMP:LOOP:I:{:.4f}:VALID".format(deviceid, i)

    @if_connected
    def get_temp_d(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:D:{:.4f}".format(deviceid, chan.d)

    @if_connected
    def set_temp_d(self, deviceid, d):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        chan.d = d
        return "STAT:SET:DEV:{}:TEMP:LOOP:D:{:.4f}:VALID".format(deviceid, d)

    @if_connected
    def get_temp_measured(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:SIG:TEMP:{:.4f}K".format(deviceid, chan.temperature)

    @if_connected
    def get_temp_setpoint(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:TSET:{:.4f}K".format(deviceid, chan.temperature_sp)

    @if_connected
    def set_temp_setpoint(self, deviceid, sp):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        chan.temperature_sp = sp
        return "STAT:SET:DEV:{}:TEMP:LOOP:TSET:{:.4f}K:VALID".format(deviceid, sp)

    @if_connected
    def get_resistance(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:SIG:RES:{:.4f}O".format(deviceid, chan.resistance)

    @if_connected
    def get_heater_auto(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:ENAB:{}".format(deviceid, "ON" if chan.heater_auto else "OFF")

    @if_connected
    def set_heater_auto(self, deviceid, sp):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        chan.heater_auto = (sp == "ON")
        return "STAT:SET:DEV:{}:TEMP:LOOP:ENAB:{}:VALID".format(deviceid, "ON" if chan.heater_auto else "OFF")

    @if_connected
    def get_gas_flow_auto(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:FAUT:{}".format(deviceid, "ON" if chan.gas_flow_auto else "OFF")

    @if_connected
    def set_gas_flow_auto(self, deviceid, sp):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        chan.gas_flow_auto = (sp == "ON")
        return "STAT:SET:DEV:{}:TEMP:LOOP:FAUT:{}:VALID".format(deviceid, "ON" if chan.gas_flow_auto else "OFF")

    @if_connected
    def get_heater_percent(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        return "STAT:DEV:{}:TEMP:LOOP:HSET:{:.4f}".format(deviceid, chan.heater_percent)

    @if_connected
    def set_heater_percent(self, deviceid, sp):
        chan = self._chan_from_id(deviceid, expected_type="TEMP")
        chan.heater_percent = sp
        return "STAT:SET:DEV:{}:TEMP:LOOP:HSET:{:.4f}:VALID".format(deviceid, sp)

    @if_connected
    def get_gas_flow(self, deviceid):
        aux_chan = self._chan_from_id(deviceid, expected_type="AUX")
        return "STAT:DEV:{}:AUX:SIG:PERC:{:.4f}".format(deviceid, aux_chan.gas_flow)

    @if_connected
    def set_gas_flow(self, deviceid, sp):
        temp_chan = self._chan_from_id(deviceid, expected_type="TEMP")
        aux_chan = self._chan_from_id(temp_chan.associated_aux_channel, expected_type="AUX")
        aux_chan.gas_flow = sp
        return "STAT:SET:DEV:{}:TEMP:LOOP:FSET:{:.4f}:VALID".format(deviceid, sp)

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
    def get_heater_voltage_limit(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="HTR")
        return "STAT:DEV:{}:HTR:VLIM:{:.4f}".format(deviceid, chan.voltage_limit)

    @if_connected
    def set_heater_voltage_limit(self, deviceid, sp):
        chan = self._chan_from_id(deviceid, expected_type="HTR")
        chan.voltage_limit = sp
        return "STAT:SET:DEV:{}:HTR:VLIM:{:.4f}:VALID".format(deviceid, chan.voltage_limit)

    @if_connected
    def get_heater_voltage(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="HTR")
        return "STAT:DEV:{}:HTR:SIG:VOLT:{:.4f}V".format(deviceid, chan.voltage)

    @if_connected
    def get_heater_current(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="HTR")
        return "STAT:DEV:{}:HTR:SIG:CURR:{:.4f}A".format(deviceid, chan.current)

    @if_connected
    def get_heater_power(self, deviceid):
        chan = self._chan_from_id(deviceid, expected_type="HTR")
        return "STAT:DEV:{}:HTR:SIG:POWR:{:.4f}W".format(deviceid, chan.power)

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
                 ":PERC:{:.4f}".format(chan.gas_flow)
