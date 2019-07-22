from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


ISOBUS_PREFIX = "@1"
DEVICE_NAME = "HelioxX"


# Format of the long-style response when querying an individual temperature card.
INDIVIDUAL_CHANNEL_RESPONSE_FORMAT = "STAT:DEV:{name}:TEMP" \
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
               ":TSET:{tset:.4f}K" \
               ":MAN:HVER:1" \
               ":FVER:1.12" \
               ":SERL:111450078" \
               ":CAL:OFFS:0" \
               ":COLDL:999.00K" \
               ":INT:LIN:SCAL:1" \
               ":FILE:None" \
               ":HOTL:999.00K" \
               ":TYPE:TCE" \
               ":SIG:VOLT:-0.0038mV" \
               ":CURR:-0.0000A" \
               ":TEMP:{temp:.4f}K" \
               ":POWR:0.0000W" \
               ":RES:0.0000O" \
               ":SLOP:0.0000O/K"


class HelioxStreamInterface(StreamInterface):
    commands = {
        CmdBuilder("get_catalog").optional(ISOBUS_PREFIX)
            .escape("READ:SYS:CAT").eos().build(),

        CmdBuilder("get_all_heliox_status").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").escape(DEVICE_NAME).escape(":HEL").eos().build(),

        CmdBuilder("get_heliox_temp").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").escape(DEVICE_NAME).escape(":HEL:SIG:TEMP").eos().build(),
        CmdBuilder("get_heliox_temp_sp_rbv").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").escape(DEVICE_NAME).escape(":HEL:SIG:TSET").eos().build(),
        CmdBuilder("get_heliox_stable").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").escape(DEVICE_NAME).escape(":HEL:SIG:H3PS").eos().build(),

        CmdBuilder("set_heliox_setpoint").optional(ISOBUS_PREFIX)
            .escape("SET:DEV:{}:HEL:SIG:TSET:".format(DEVICE_NAME)).float().escape("K").eos().build(),

        CmdBuilder("get_nickname").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:").any().escape(":NICK").eos().build(),

        CmdBuilder("get_all_he3_sorb_status").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:He3Sorb:TEMP").eos().build(),
        CmdBuilder("get_all_he4_pot_status").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:He4Pot:TEMP").eos().build(),
        CmdBuilder("get_all_he_high_status").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:HeHigh:TEMP").eos().build(),
        CmdBuilder("get_all_he_low_status").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:HeLow:TEMP").eos().build(),

        CmdBuilder("get_he3_sorb_temp").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:He3Sorb:TEMP:SIG:TEMP").eos().build(),
        CmdBuilder("get_he4_pot_temp").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:He4Pot:TEMP:SIG:TEMP").eos().build(),
        CmdBuilder("get_he_high_temp").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:HeHigh:TEMP:SIG:TEMP").eos().build(),
        CmdBuilder("get_he_low_temp").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:HeLow:TEMP:SIG:TEMP").eos().build(),

        CmdBuilder("get_he3_sorb_temp_sp").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:He3Sorb:TEMP:LOOP:TSET").eos().build(),
        CmdBuilder("get_he4_pot_temp_sp").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:He4Pot:TEMP:LOOP:TSET").eos().build(),
        CmdBuilder("get_he_high_temp_sp").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:HeHigh:TEMP:LOOP:TSET").eos().build(),
        CmdBuilder("get_he_low_temp_sp").optional(ISOBUS_PREFIX)
            .escape("READ:DEV:HeLow:TEMP:LOOP:TSET").eos().build(),
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    def get_all_heliox_status(self):
        """
        This function is used by the labview VI. In EPICS it is more convenient to ask for the parameters individually,
        so we don't use this large function which generates all of the possible status information.
        """
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
               ":TEMP:{:.4f}K".format(self.device.temperature) + \
               ":TSET:{:.4f}K".format(self.device.temperature_sp) + \
               ":H3PS:{}".format("Stable" if self.device.temperature_stable else "Unstable") + \
               ":SRBS:Stable" \
               ":SRBR:32.000K" \
               ":SCT:3.0000K" \
               ":NVLT:10.000mB"

    def get_catalog(self):
        """
        This is only needed by the LabVIEW driver - it is not used by EPICS.
        """
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

    def get_all_he3_sorb_status(self):
        return INDIVIDUAL_CHANNEL_RESPONSE_FORMAT.format(
            name="He3Sorb",
            tset=self.device.temperature_channels["HE3SORB"].temperature_sp,
            temp=self.device.temperature_channels["HE3SORB"].temperature,
        )

    def get_all_he4_pot_status(self):
        return INDIVIDUAL_CHANNEL_RESPONSE_FORMAT.format(
            name="He4Pot",
            tset=self.device.temperature_channels["HE4POT"].temperature_sp,
            temp=self.device.temperature_channels["HE4POT"].temperature,
        )

    def get_all_he_high_status(self):
        return INDIVIDUAL_CHANNEL_RESPONSE_FORMAT.format(
            name="HeHigh",
            tset=self.device.temperature_channels["HEHIGH"].temperature_sp,
            temp=self.device.temperature_channels["HEHIGH"].temperature,
        )

    def get_all_he_low_status(self):
        return INDIVIDUAL_CHANNEL_RESPONSE_FORMAT.format(
            name="HeLow",
            tset=self.device.temperature_channels["HELOW"].temperature_sp,
            temp=self.device.temperature_channels["HELOW"].temperature,
        )

    def set_heliox_setpoint(self, new_setpoint):
        self.device.temperature_sp = new_setpoint
        return self.get_heliox_temp_sp_rbv()

    def get_heliox_temp(self):
        return "STAT:DEV:HelioxX:HEL:SIG:TEMP:{:.4f}K".format(self.device.temperature)

    def get_heliox_temp_sp_rbv(self):
        return "STAT:DEV:HelioxX:HEL:SIG:TSET:{:.4f}K".format(self.device.temperature_sp)

    def get_heliox_stable(self):
        return "STAT:DEV:{}:HEL:SIG:H3PS:{}".format(DEVICE_NAME, "Stable" if self.device.temperature_stable else "Unstable")

    def get_he3_sorb_temp(self):
        return "STAT:DEV:He3Sorb:TEMP:SIG:TEMP:{:.4f}K".format(self.device.temperature_channels["HE3SORB"].temperature)

    def get_he4_pot_temp(self):
        return "STAT:DEV:He4Pot:TEMP:SIG:TEMP:{:.4f}K".format(self.device.temperature_channels["HE4POT"].temperature)

    def get_he_low_temp(self):
        return "STAT:DEV:HeLow:TEMP:SIG:TEMP:{:.4f}K".format(self.device.temperature_channels["HELOW"].temperature)

    def get_he_high_temp(self):
        return "STAT:DEV:HeHigh:TEMP:SIG:TEMP:{:.4f}K".format(self.device.temperature_channels["HEHIGH"].temperature)

    def get_he3_sorb_temp_sp(self):
        return "STAT:DEV:He3Sorb:TEMP:LOOP:TSET:{:.4f}K".format(self.device.temperature_channels["HE3SORB"].temperature_sp)

    def get_he4_pot_temp_sp(self):
        return "STAT:DEV:He4Pot:TEMP:LOOP:TSET:{:.4f}K".format(self.device.temperature_channels["HE4POT"].temperature_sp)

    def get_he_low_temp_sp(self):
        return "STAT:DEV:HeLow:TEMP:LOOP:TSET:{:.4f}K".format(self.device.temperature_channels["HELOW"].temperature_sp)

    def get_he_high_temp_sp(self):
        return "STAT:DEV:HeHigh:TEMP:LOOP:TSET:{:.4f}K".format(self.device.temperature_channels["HEHIGH"].temperature_sp)
