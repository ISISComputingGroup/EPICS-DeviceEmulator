from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


ISOBUS_PREFIX = "@1"
DEVICE_NAME = "HelioxX"


class HelioxStreamInterface(StreamInterface):
    commands = {
        CmdBuilder("get_catalog")
            .escape(ISOBUS_PREFIX).escape("READ:SYS:CAT").eos().build(),

        CmdBuilder("set_heliox_setpoint")
            .escape(ISOBUS_PREFIX).escape("SET:DEV:{}:HEL:SIG:TSET:".format(DEVICE_NAME)).float().escape("K").eos().build(),
        CmdBuilder("get_heliox_status")
            .escape(ISOBUS_PREFIX).escape("READ:DEV:").escape(DEVICE_NAME).escape(":HEL").eos().build(),

        CmdBuilder("get_nickname")
            .escape(ISOBUS_PREFIX).escape("READ:DEV:").any().escape(":NICK").eos().build(),

        CmdBuilder("get_he3_sorb_temp")
            .escape(ISOBUS_PREFIX).escape("READ:DEV:He3Sorb:TEMP").eos().build(),
        CmdBuilder("get_he4_pot_temp")
            .escape(ISOBUS_PREFIX).escape("READ:DEV:He4Pot:TEMP").eos().build(),
        CmdBuilder("get_he_high_temp")
            .escape(ISOBUS_PREFIX).escape("READ:DEV:HeHigh:TEMP").eos().build(),
        CmdBuilder("get_he_low_temp")
            .escape(ISOBUS_PREFIX).escape("READ:DEV:HeLow:TEMP").eos().build(),
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    def get_heliox_status(self):
        return "STAT:DEV:{}".format(DEVICE_NAME) + \
               ":HEL:LOWT:2.5000K" \
               ":BT:0.0000K" \
               ":NVCN:17.000mB" \
               ":RCTD:10.000K" \
               ":RCST:20.000K" \
               ":NVHT:17.000mB" \
               ":RCTE:10.000K" \
               ":SRBH:15.000K" \
               ":PE:3.5000K" \
               ":RGNA:1.0000K" \
               ":PCT:2.0000K" \
               ":SIG:H4PS:Stable" \
               ":STAT:Regenerate" \
               ":TEMP:{}K".format(self.device.temperature) + \
               ":TSET:{}K".format(self.device.temperature_sp) + \
               ":H3PS:Stable" \
               ":SRBS:Stable" \
               ":SRBR:32.000K" \
               ":SCT:3.0000K" \
               ":NVLT:10.000mB"

    def get_catalog(self):
        return "STAT:SYS:CAT" \
               ":DEV:HelioxX:HEL" \
               ":DEV:He3Sorb:TEMP" \
               ":DEV:He4Pot:TEMP" \
               ":DEV:HeLow:TEMP" \
               ":DEV:HeHigh:TEMP"

    def get_nickname(self, arg):
        """
        Returns a fake nickname. This is only implemented to allow this emulator to be used with the existing
        labview driver, and the labview driver actually ignores the results (but not implementing the function causes
        an error).
        """
        return "STAT:DEV:{}:NICK:{}".format(arg, "FAKENICKNAME")

    def get_he3_sorb_temp(self):
        return "STAT:DEV:He3Sorb:TEMP" \
               ":EXCT:TYPE:UNIP:MAG:0" \
               ":STAT:40000000" \
               ":NICK:MB1.T1" \
               ":LOOP:AUX:None" \
               ":D:1.0" \
               ":HTR:None" \
               ":I:1.0" \
               ":THTF:None" \
               ":HSET:0" \
               ":PIDT:OFF" \
               ":ENAB:OFF" \
               ":SWFL:None" \
               ":FAUT:OFF" \
               ":FSET:0" \
               ":PIDF:None" \
               ":P:1.0" \
               ":SWMD:FIX" \
               ":TSET:0.0000K" \
               ":MAN:HVER:1" \
               ":FVER:1.12" \
               ":SERL:111450078" \
               ":CAL:OFFS:0" \
               ":COLDL:999.00K" \
               ":INT:LIN:SCAL:1" \
               ":FILE:None" \
               ":HOTL:999.00K" \
               ":TYPE:TCE:SIG:VOLT:-0.0038mV" \
               ":CURR:-0.0000A" \
               ":TEMP:1.2345K" \
               ":POWR:0.0000W" \
               ":RES:0.0000O" \
               ":SLOP:0.0000O/K"

    def get_he4_pot_temp(self):
        return "STAT:DEV:He4Pot:TEMP" \
               ":EXCT:TYPE:UNIP:MAG:0" \
               ":STAT:40000000" \
               ":NICK:MB1.T1" \
               ":LOOP:AUX:None" \
               ":D:1.0" \
               ":HTR:None" \
               ":I:1.0" \
               ":THTF:None" \
               ":HSET:0" \
               ":PIDT:OFF" \
               ":ENAB:OFF" \
               ":SWFL:None" \
               ":FAUT:OFF" \
               ":FSET:0" \
               ":PIDF:None" \
               ":P:1.0" \
               ":SWMD:FIX" \
               ":TSET:0.0000K" \
               ":MAN:HVER:1" \
               ":FVER:1.12" \
               ":SERL:111450078" \
               ":CAL:OFFS:0" \
               ":COLDL:999.00K" \
               ":INT:LIN:SCAL:1" \
               ":FILE:None" \
               ":HOTL:999.00K" \
               ":TYPE:TCE:SIG:VOLT:-0.0038mV" \
               ":CURR:-0.0000A" \
               ":TEMP:2.3456K" \
               ":POWR:0.0000W" \
               ":RES:0.0000O" \
               ":SLOP:0.0000O/K"

    def get_he_low_temp(self):
        return "STAT:DEV:HeLow:TEMP" \
               ":EXCT:TYPE:UNIP:MAG:0" \
               ":STAT:40000000" \
               ":NICK:MB1.T1" \
               ":LOOP:AUX:None" \
               ":D:1.0" \
               ":HTR:None" \
               ":I:1.0" \
               ":THTF:None" \
               ":HSET:0" \
               ":PIDT:OFF" \
               ":ENAB:OFF" \
               ":SWFL:None" \
               ":FAUT:OFF" \
               ":FSET:0" \
               ":PIDF:None" \
               ":P:1.0" \
               ":SWMD:FIX" \
               ":TSET:0.0000K" \
               ":MAN:HVER:1" \
               ":FVER:1.12" \
               ":SERL:111450078" \
               ":CAL:OFFS:0" \
               ":COLDL:999.00K" \
               ":INT:LIN:SCAL:1" \
               ":FILE:None" \
               ":HOTL:999.00K" \
               ":TYPE:TCE:SIG:VOLT:-0.0038mV" \
               ":CURR:-0.0000A" \
               ":TEMP:3.4567K" \
               ":POWR:0.0000W" \
               ":RES:0.0000O" \
               ":SLOP:0.0000O/K"

    def get_he_high_temp(self):
        return "STAT:DEV:HeHigh:TEMP" \
               ":EXCT:TYPE:UNIP:MAG:0" \
               ":STAT:40000000" \
               ":NICK:MB1.T1" \
               ":LOOP:AUX:None" \
               ":D:1.0" \
               ":HTR:None" \
               ":I:1.0" \
               ":THTF:None" \
               ":HSET:0" \
               ":PIDT:OFF" \
               ":ENAB:OFF" \
               ":SWFL:None" \
               ":FAUT:OFF" \
               ":FSET:0" \
               ":PIDF:None" \
               ":P:1.0" \
               ":SWMD:FIX" \
               ":TSET:0.0000K" \
               ":MAN:HVER:1" \
               ":FVER:1.12" \
               ":SERL:111450078" \
               ":CAL:OFFS:0" \
               ":COLDL:999.00K" \
               ":INT:LIN:SCAL:1" \
               ":FILE:None" \
               ":HOTL:999.00K" \
               ":TYPE:TCE:SIG:VOLT:-0.0038mV" \
               ":CURR:-0.0000A" \
               ":TEMP:4.5678K" \
               ":POWR:0.0000W" \
               ":RES:0.0000O" \
               ":SLOP:0.0000O/K"

    def set_heliox_setpoint(self, new_setpoint):
        self.device.temperature_sp = new_setpoint
