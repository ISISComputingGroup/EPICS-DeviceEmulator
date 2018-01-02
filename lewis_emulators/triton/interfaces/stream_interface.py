from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.triton.device import HEATER_NAME
from lewis_emulators.triton.device import ValveStates


@has_log
class TritonStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        # UIDs
        CmdBuilder("get_mc_uid").escape("READ:SYS:DR:CHAN:MC").build(),
        CmdBuilder("get_stil_uid").escape("READ:SYS:DR:CHAN:STIL").build(),
        CmdBuilder("get_sorb_uid").escape("READ:SYS:DR:CHAN:SORB").build(),

        # PID setpoints
        CmdBuilder("set_p").escape("SET:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:P:").float().build(),
        CmdBuilder("set_i").escape("SET:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:I:").float().build(),
        CmdBuilder("set_d").escape("SET:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:D:").float().build(),

        # PID readbacks
        CmdBuilder("get_p").escape("READ:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:P").build(),
        CmdBuilder("get_i").escape("READ:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:I").build(),
        CmdBuilder("get_d").escape("READ:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:D").build(),

        # Setpoint temperature
        CmdBuilder("set_temperature_setpoint")
            .escape("SET:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:TSET:").float().build(),
        CmdBuilder("get_temperature_setpoint").escape("READ:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:TSET").build(),

        # Temperature
        CmdBuilder("get_temp").escape("READ:DEV:").arg("T[0-9]+").escape(":TEMP:SIG:TEMP").build(),

        # Heater range
        CmdBuilder("set_heater_range").escape("SET:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:RANGE:").float().build(),
        CmdBuilder("get_heater_range").escape("READ:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:RANGE").build(),

        # Heater type
        CmdBuilder("get_heater_type").escape("READ:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:HTR").build(),

        # Get heater power
        CmdBuilder("get_heater_power").escape("READ:DEV:{}:HTR:SIG:POWR".format(HEATER_NAME)).build(),

        # Loop mode
        CmdBuilder("get_closed_loop_mode").escape("READ:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:MODE").build(),
        CmdBuilder("set_closed_loop_mode").escape("SET:DEV:").arg("T[0-9]+").escape(":TEMP:LOOP:MODE:").any().build(),

        # Valve state
        CmdBuilder("get_valve_state").escape("READ:DEV:").arg("V[0-9]+").escape(":VALV:SIG:STATE").build(),

        # Channel enablement
        CmdBuilder("get_channel_enabled").escape("READ:DEV:").arg("T[0-9]+").escape(":TEMP:MEAS:ENAB").build(),
        CmdBuilder("set_channel_enabled").escape("SET:DEV:").arg("T[0-9]+").escape(":TEMP:MEAS:ENAB:").any().build(),

        # Status
        CmdBuilder("get_status").escape("READ:SYS:DR:STATUS").build(),
        CmdBuilder("get_automation").escape("READ:SYS:DR:ACTN").build(),

        # Pressures
        CmdBuilder("get_pressure").escape("READ:DEV:").arg("P[0-9]+").escape(":PRES:SIG:PRES").build(),
    }

    in_terminator = "\r\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}\n".format(request, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    def raise_if_channel_is_not_mc_channel(self, chan):
        if str(chan) != self.device.find_temperature_channel("mc"):
            raise ValueError("Channel should have been MC channel")

    def get_mc_uid(self):
        return "STAT:SYS:DR:CHAN:MC:{}".format(self.device.find_temperature_channel("mc"))

    def get_stil_uid(self):
        return "STAT:SYS:DR:CHAN:STIL:{}".format(self.device.find_temperature_channel("stil"))

    def get_sorb_uid(self):
        return "STAT:SYS:DR:CHAN:SORB:{}".format(self.device.find_temperature_channel("sorb"))

    def set_p(self, stage, value):
        self.raise_if_channel_is_not_mc_channel(stage)
        self.device.set_p(float(value))
        return "ok"

    def set_i(self, stage, value):
        self.raise_if_channel_is_not_mc_channel(stage)
        self.device.set_i(float(value))
        return "ok"

    def set_d(self, stage, value):
        self.raise_if_channel_is_not_mc_channel(stage)
        self.device.set_d(float(value))
        return "ok"

    def get_p(self, stage):
        self.raise_if_channel_is_not_mc_channel(stage)
        return "STAT:DEV:{}:TEMP:LOOP:P:{}".format(stage, self.device.get_p())

    def get_i(self, stage):
        self.raise_if_channel_is_not_mc_channel(stage)
        return "STAT:DEV:{}:TEMP:LOOP:I:{}".format(stage, self.device.get_i())

    def get_d(self, stage):
        self.raise_if_channel_is_not_mc_channel(stage)
        return "STAT:DEV:{}:TEMP:LOOP:D:{}".format(stage, self.device.get_d())

    def set_temperature_setpoint(self, chan, value):
        self.raise_if_channel_is_not_mc_channel(chan)
        self.device.set_temperature_setpoint(float(value))
        return "ok"

    def get_temperature_setpoint(self, chan):
        self.raise_if_channel_is_not_mc_channel(chan)
        return "STAT:DEV:{}:TEMP:LOOP:TSET:{}K" \
            .format(self.device.find_temperature_channel("mc"), self.device.get_temperature_setpoint())

    def set_heater_range(self, chan, value):
        self.raise_if_channel_is_not_mc_channel(chan)
        self.device.set_heater_range(float(value))
        return "ok"

    def get_heater_range(self, chan):
        self.raise_if_channel_is_not_mc_channel(chan)
        return "STAT:DEV:{}:TEMP:LOOP:RANGE:{}".format(chan, self.device.get_heater_range())

    def get_heater_type(self, chan):
        self.raise_if_channel_is_not_mc_channel(chan)
        return "STAT:DEV:{}:TEMP:LOOP:HTR:{}".format(chan, HEATER_NAME)

    def get_heater_power(self):
        return "STAT:DEV:{}:HTR:SIG:POWR:{}{}"\
            .format(HEATER_NAME, self.device.heater_power, self.device.heater_power_units)

    def get_closed_loop_mode(self, chan):
        self.raise_if_channel_is_not_mc_channel(chan)
        return "STAT:DEV:{}:TEMP:LOOP:MODE:{}".format(chan, "ON" if self.device.get_closed_loop_mode() else "OFF")

    def set_closed_loop_mode(self, chan, mode):
        self.raise_if_channel_is_not_mc_channel(chan)

        if mode not in ["ON", "OFF"]:
            raise ValueError("Invalid mode")

        self.device.set_closed_loop_mode(mode == "ON")
        return "ok"

    def get_valve_state(self, valve):

        state = self.device.get_valve_state(valve)

        if state == ValveStates.CLOSED:
            response = "CLOSE"
        elif state == ValveStates.OPEN:
            response = "OPEN"
        elif state == ValveStates.NOT_FOUND:
            response = "NOT_FOUND"
        else:
            raise ValueError("Invalid valve state: {}".format(state))

        return "STAT:DEV:{}:VALV:SIG:STATE:{}".format(valve, response)

    def get_channel_enabled(self, channel):
        return "STAT:DEV:{}:TEMP:MEAS:ENAB:{}"\
            .format(channel, "ON" if self.device.is_channel_enabled(channel) else "OFF")

    def set_channel_enabled(self, channel, newstate):
        newstate = str(newstate)

        if newstate not in ["ON", "OFF"]:
            raise ValueError("New state '{}' not valid.".format(newstate))

        self.device.set_channel_enabled(channel, newstate == "ON")
        return "ok"

    def get_status(self):
        return "STAT:SYS:DR:STATUS:{}".format(self.device.get_status())

    def get_automation(self):
        return "STAT:SYS:DR:ACTN:{}".format(self.device.get_automation())

    def get_temp(self, stage):
        return "STAT:DEV:{}:TEMP:SIG:TEMP:{}K".format(stage, self.device.get_temp(str(stage)))

    def get_pressure(self, sensor):
        return "STAT:DEV:{}:PRES:SIG:PRES:{}mB".format(sensor, self.device.get_pressure(sensor))
