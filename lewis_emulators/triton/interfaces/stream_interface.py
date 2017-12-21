from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.triton.device import SUBSYSTEM_NAMES
from lewis_emulators.triton.device import ValveStates


@has_log
class TritonStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        # UIDs
        CmdBuilder("get_mc_uid")
            .escape("READ:SYS:DR:CHAN:MC").build(),
        CmdBuilder("get_stil_uid")
            .escape("READ:SYS:DR:CHAN:STIL").build(),
        CmdBuilder("get_sorb_uid")
            .escape("READ:SYS:DR:CHAN:SORB").build(),

        # PID setpoints
        CmdBuilder("set_p")
            .escape("SET:DEV:").arg("T[0-9]").escape(":TEMP:LOOP:P:").float().build(),
        CmdBuilder("set_i")
            .escape("SET:DEV:").arg("T[0-9]").escape(":TEMP:LOOP:I:").float().build(),
        CmdBuilder("set_d")
            .escape("SET:DEV:").arg("T[0-9]").escape(":TEMP:LOOP:D:").float().build(),

        # PID readbacks
        CmdBuilder("get_p")
            .escape("READ:DEV:").arg("T[0-9]").escape(":TEMP:LOOP:P").build(),
        CmdBuilder("get_i")
            .escape("READ:DEV:").arg("T[0-9]").escape(":TEMP:LOOP:I").build(),
        CmdBuilder("get_d")
            .escape("READ:DEV:").arg("T[0-9]").escape(":TEMP:LOOP:D").build(),

        # Setpoint temperature
        CmdBuilder("set_temperature_setpoint")
            .escape("SET:DEV:{}:TEMP:LOOP:TSET:".format(SUBSYSTEM_NAMES["mixing chamber"])).float().build(),
        CmdBuilder("get_temperature_setpoint")
            .escape("READ:DEV:{}:TEMP:LOOP:TSET".format(SUBSYSTEM_NAMES["mixing chamber"])).build(),

        # Temperature
        CmdBuilder("get_temp")
            .escape("READ:DEV:").arg("T[0-9]").escape(":TEMP:SIG:TEMP").build(),

        # Heater range
        CmdBuilder("set_heater_range")
            .escape("SET:DEV:{}:TEMP:LOOP:RANGE:".format(SUBSYSTEM_NAMES["mixing chamber"])).float().build(),
        CmdBuilder("get_heater_range")
            .escape("READ:DEV:{}:TEMP:LOOP:RANGE".format(SUBSYSTEM_NAMES["mixing chamber"])).build(),

        # Heater type
        CmdBuilder("get_heater_type")
            .escape("READ:DEV:{}:TEMP:LOOP:HTR".format(SUBSYSTEM_NAMES["mixing chamber"])).build(),

        # Get heater power
        CmdBuilder("get_heater_power")
            .escape("READ:DEV:{}:HTR:SIG:POWR".format(SUBSYSTEM_NAMES["heater"])).build(),

        # Loop mode
        CmdBuilder("get_closed_loop_mode")
            .escape("READ:DEV:{}:TEMP:LOOP:MODE".format(SUBSYSTEM_NAMES["mixing chamber"])).build(),
        CmdBuilder("set_closed_loop_mode")
            .escape("SET:DEV:{}:TEMP:LOOP:MODE:".format(SUBSYSTEM_NAMES["mixing chamber"])).any().build(),

        # Valve state
        CmdBuilder("get_valve_state")
            .escape("READ:DEV:V").int().escape(":VALV:SIG:STATE").build(),

        # Channel enablement
        CmdBuilder("get_channel_enabled")
            .escape("READ:DEV:T").int().escape(":TEMP:MEAS:ENAB").build(),
        CmdBuilder("set_channel_enabled")
            .escape("SET:DEV:T").int().escape(":TEMP:MEAS:ENAB:").any().build(),

        # Status
        CmdBuilder("get_status")
            .escape("READ:SYS:DR:STATUS").build(),

        # Automation
        CmdBuilder("get_automation")
            .escape("READ:SYS:DR:ACTN").build(),

        # Pressures
        CmdBuilder("get_pressure")
            .escape("READ:DEV:").arg("P[0-9]").escape(":PRES:SIG:PRES").build(),
    }

    in_terminator = "\r\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}\n".format(request, error)
        print(err_string)
        # self.log.error(err)
        return err_string

    def get_mc_uid(self):
        return "STAT:SYS:DR:CHAN:MC:{}".format(self.device.find_temperature_channel("mc"))

    def get_stil_uid(self):
        return "STAT:SYS:DR:CHAN:STIL:{}".format(self.device.find_temperature_channel("stil"))

    def get_sorb_uid(self):
        return "STAT:SYS:DR:CHAN:SORB:{}".format(self.device.find_temperature_channel("sorb"))

    def set_p(self, stage, value):
        self.device.set_p(stage, float(value))
        return "ok"

    def set_i(self, stage, value):
        self.device.set_i(stage, float(value))
        return "ok"

    def set_d(self, stage, value):
        self.device.set_d(stage, float(value))
        return "ok"

    def get_p(self, stage):
        return "STAT:DEV:{}:TEMP:LOOP:P:{}" \
            .format(stage, self.device.get_p(stage))

    def get_i(self, stage):
        return "STAT:DEV:{}:TEMP:LOOP:I:{}" \
            .format(stage, self.device.get_i(stage))

    def get_d(self, stage):
        return "STAT:DEV:{}:TEMP:LOOP:D:{}" \
            .format(stage, self.device.get_d(stage))

    def set_temperature_setpoint(self, value):
        self.device.set_temperature_setpoint(float(value))
        return "ok"

    def get_temperature_setpoint(self):
        return "STAT:DEV:{}:TEMP:LOOP:TSET:{}K" \
            .format(self.device.find_temperature_channel("mc"), self.device.get_temperature_setpoint())

    def set_heater_range(self, value):
        self.device.set_heater_range(float(value))
        return "ok"

    def get_heater_range(self):
        return "STAT:DEV:{}:TEMP:LOOP:RANGE:{}" \
            .format(self.device.find_temperature_channel("mc"), self.device.get_heater_range())

    def get_heater_type(self):
        return "STAT:DEV:{}:TEMP:LOOP:HTR:{}" \
            .format(self.device.find_temperature_channel("mc"), SUBSYSTEM_NAMES["heater"])

    def get_heater_power(self):
        return "STAT:DEV:{}:HTR:SIG:POWR:{}{}"\
            .format(SUBSYSTEM_NAMES["heater"], self.device.heater_power, self.device.heater_power_units)

    def get_closed_loop_mode(self):
        return "STAT:DEV:{}:TEMP:LOOP:MODE:{}"\
            .format(self.device.find_temperature_channel("mc"), "ON" if self.device.get_closed_loop_mode() else "OFF")

    def set_closed_loop_mode(self, mode):
        if mode not in ["ON", "OFF"]:
            raise ValueError("Invalid mode")

        self.device.set_closed_loop_mode(mode == "ON")
        return "ok"

    def get_valve_state(self, valve):

        state = self.device.get_valve_state(int(valve))

        if state == ValveStates.CLOSED:
            response = "CLOSE"
        elif state == ValveStates.OPEN:
            response = "OPEN"
        elif state == ValveStates.NOT_FOUND:
            response = "NOT_FOUND"
        else:
            raise ValueError("Invalid valve state: {}".format(state))

        return "STAT:DEV:V{}:VALV:SIG:STATE:{}".format(valve, response)

    def get_channel_enabled(self, channel):
        return "STAT:DEV:T{}:TEMP:MEAS:ENAB:{}"\
            .format(channel, "ON" if self.device.is_channel_enabled(int(channel)) else "OFF")

    def set_channel_enabled(self, channel, newstate):
        if newstate not in ["ON", "OFF"]:
            raise ValueError("New state '{}' not valid.".format(newstate))
        self.device.set_channel_enabled(int(channel), str(newstate) == "ON")
        return "ok"

    def get_status(self):
        return "STAT:SYS:DR:STATUS:{}".format(self.device.get_status())

    def get_automation(self):
        return "STAT:SYS:DR:ACTN:{}".format(self.device.get_automation())

    def get_temp(self, stage):
        return "STAT:DEV:{}:TEMP:SIG:TEMP:{}K".format(stage, self.device.get_temp(str(stage)))

    def get_pressure(self, sensor):
        return "STAT:DEV:{}:PRES:SIG:PRES:{}mB".format(sensor, self.device.get_pressure(sensor))
