from contextlib import contextmanager

from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder


def add_terminator(terminator="\r\n"):
    """
    This is a slight hack because:
    - Lewis doesn't support dynamically changing terminators
    - The induction furnace "forgets" to add the terminator to at least one command's response.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            return "{}{}".format(func(*args, **kwargs), terminator)
        return wrapper
    return decorator


@has_log
class IndfurnStreamInterface(StreamInterface):
    commands = {
        # ID
        CmdBuilder("get_version").escape("?ver").eos().build(),

        CmdBuilder("get_setpoint").escape("?pidSP").eos().build(),
        CmdBuilder("set_setpoint").escape(">pidSP ").float().eos().build(),

        CmdBuilder("get_psu_voltage").escape("?powV").eos().build(),
        CmdBuilder("set_psu_voltage").escape(">powV ").float().eos().build(),

        CmdBuilder("get_psu_current").escape("?powI").eos().build(),
        CmdBuilder("set_psu_current").escape(">powI ").float().eos().build(),

        CmdBuilder("get_output").escape("?pidOUTM").eos().build(),
        CmdBuilder("set_output").escape(">pidOUTM ").float().eos().build(),

        CmdBuilder("get_thermocouple_temperature").escape("?tempTC").eos().build(),
        CmdBuilder("get_pipe_temperature").escape("?tempP").eos().build(),
        CmdBuilder("get_capacitor_bank_temperature").escape("?tempC").eos().build(),
        CmdBuilder("get_fet_temperature").escape("?tempS").eos().build(),

        CmdBuilder("get_pid_params").escape("?pidTu").eos().build(),
        CmdBuilder("set_pid_params").escape(">pidTu ").float().escape(" ").float().escape(" ").float().eos().build(),

        CmdBuilder("get_sample_time").escape("?pidSt").eos().build(),
        CmdBuilder("set_sample_time").escape(">pidSt ").int().eos().build(),

        CmdBuilder("get_psu_direction").escape("?pidDir").eos().build(),
        CmdBuilder("set_psu_direction").escape(">pidDir ").any().eos().build(),

        CmdBuilder("get_pid_mode").escape("?pidMODE").eos().build(),
        CmdBuilder("set_pid_mode").escape(">pidMODE ").char().eos().build(),

        CmdBuilder("set_psu_remote").escape(">powR").eos().build(),
        CmdBuilder("set_psu_local").escape(">powL").eos().build(),
        CmdBuilder("get_psu_control_mode").escape("?powRL").eos().build(),

        CmdBuilder("set_psu_on").escape(">powON").eos().build(),
        CmdBuilder("set_psu_off").escape(">powOFF").eos().build(),
        CmdBuilder("get_psu_power").escape("?powOnOff").eos().build(),

        CmdBuilder("set_psu_fan_on").escape(">fanON").eos().build(),
        CmdBuilder("set_psu_fan_off").escape(">fanOFF").eos().build(),
        CmdBuilder("get_fan_power").escape("?fanOnOff").eos().build(),

        CmdBuilder("set_hf_on").escape(">oscON").eos().build(),
        CmdBuilder("set_hf_off").escape(">oscOFF").eos().build(),
        CmdBuilder("get_hf_power").escape("?oscOnOff").eos().build(),

        CmdBuilder("get_pid_limits").escape("?pidOUTL").eos().build(),
        CmdBuilder("set_pid_limits").escape(">pidOUTL ").float().escape(" ").float().eos().build(),

        CmdBuilder("get_psu_overtemp").escape("?alarmh").eos().build(),
        CmdBuilder("get_psu_overvolt").escape("?alarmv").eos().build(),
        CmdBuilder("get_cooling_water_flow_status").escape("?flowSt").eos().build(),
        CmdBuilder("get_cooling_water_flow").escape("?flowCw").eos().build(),
        CmdBuilder("reset_alarms").escape(">ackAlarm").eos().build(),

        CmdBuilder("set_runmode_on").escape(">pidRUN").eos().build(),
        CmdBuilder("set_runmode_off").escape(">pidSTP").eos().build(),
        CmdBuilder("get_runmode").escape("?pidRUN").eos().build(),
    }

    in_terminator = "\r\n"
    readtimeout = 25
    out_terminator = ""  # We add our terminators explicitly as they are variable.

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return "<Unsupported command"

    @add_terminator()
    def get_pid_mode(self):
        return "<pmode {}".format("a" if self.device.pid_mode_automatic else "m")

    @add_terminator()
    def set_pid_mode(self, pid_mode):
        if pid_mode == "a":
            self.device.pid_mode_automatic = True
            return "<ack"
        elif pid_mode == "m":
            self.device.pid_mode_automatic = False
            return "<ack"
        else:
            return "<nak"

    @add_terminator()
    def get_version(self):
        name = "EMULATED FURNACE"
        return "<{name}{terminator}<{name}".format(name=name, terminator="\r\n")

    @add_terminator()
    def get_setpoint(self):
        return "<pidsp {:.2f}".format(self.device.setpoint)

    @add_terminator()
    def set_setpoint(self, sp):
        self.device.setpoint = float(sp)
        return "<ack"

    @add_terminator()
    def get_psu_voltage(self):
        return "<powv {:.2f}".format(self.device.psu_voltage)

    @add_terminator()
    def set_psu_voltage(self, voltage):
        self.device.psu_voltage = float(voltage)
        return "<ack"

    @add_terminator()
    def get_psu_current(self):
        return "<powa {:.2f}".format(self.device.psu_current)

    @add_terminator()
    def set_psu_current(self, current):
        self.device.psu_current = float(current)
        return "<ack"

    @add_terminator(terminator="")
    def get_output(self):
        return "<pidoutm {:.2f}".format(self.device.output)

    @add_terminator()
    def set_output(self, output):
        self.device.output = float(output)
        return "<ack"

    @add_terminator()
    def get_thermocouple_temperature(self):
        return "<temptc {:.2f}".format(self.device.setpoint)

    @add_terminator()
    def get_pipe_temperature(self):
        return "<tempp {:.2f}".format(self.device.pipe_temperature)

    @add_terminator()
    def get_capacitor_bank_temperature(self):
        return "<tempc {:.2f}".format(self.device.capacitor_bank_temperature)

    @add_terminator()
    def get_fet_temperature(self):
        return "<temps {:.2f}".format(self.device.fet_temperature)

    @add_terminator()
    def get_pid_params(self):
        return "<pidtu {:.2f} {:.2f} {:.2f}".format(self.device.p, self.device.i, self.device.d)

    @add_terminator()
    def set_pid_params(self, p, i, d):
        self.device.p = float(p)
        self.device.i = float(i)
        self.device.d = float(d)
        return "<ack"

    @add_terminator()
    def get_pid_limits(self):
        return "<PID out limit min max:  {:.2f} {:.2f}".format(self.device.pid_lower_limit, self.device.pid_upper_limit)

    @add_terminator()
    def set_pid_limits(self, pid_lower_limit, pid_upper_limit):
        self.device.pid_lower_limit = float(pid_lower_limit)
        self.device.pid_upper_limit = float(pid_upper_limit)
        return "<ack"

    @add_terminator()
    def get_sample_time(self):
        return "<pidst {:d}".format(self.device.sample_time)

    @add_terminator()
    def set_sample_time(self, sample_time):
        self.device.sample_time = int(sample_time)
        return "<ack"

    @add_terminator()
    def get_psu_direction(self):
        return "<piddir {}".format("p" if self.device.direction_heating else "n")

    @add_terminator()
    def set_psu_direction(self, direction):
        if direction == "DIR":
            self.device.direction_heating = True
            return "<ack"
        elif direction == "REV":
            self.device.direction_heating = False
            return "<ack"
        else:
            return "<nak"

    @add_terminator()
    def get_psu_overtemp(self):
        return "<{}".format("on" if self.device.psu_overtemp else "off")

    @add_terminator()
    def get_psu_overvolt(self):
        return "<{}".format("on" if self.device.psu_overvolt else "off")

    @add_terminator()
    def get_cooling_water_flow_status(self):
        return "<{}".format("ok" if self.device.is_cooling_water_flow_ok() else "nok")

    @add_terminator()
    def get_cooling_water_flow(self):
        return "<flow {}".format(self.device.cooling_water_flow)

    @add_terminator()
    def reset_alarms(self):
        self.device.psu_overtemp = False
        self.device.psu_overvolt = False
        return "<ack"

    @add_terminator()
    def set_psu_remote(self):
        self.device.remote_mode = True
        return "<ack"

    @add_terminator()
    def set_psu_local(self):
        self.device.remote_mode = False
        return "<ack"

    @add_terminator()
    def set_psu_on(self):
        self.device.power_supply_on = True
        return "<ack"

    @add_terminator()
    def set_psu_off(self):
        self.device.power_supply_on = False
        return "<ack"

    @add_terminator()
    def set_psu_fan_on(self):
        self.device.power_supply_fan_on = True
        return "<ack"

    @add_terminator()
    def set_psu_fan_off(self):
        self.device.power_supply_fan_on = False
        return "<ack"

    @add_terminator()
    def set_hf_on(self):
        self.device.hf_on = True
        return "<ack"

    @add_terminator()
    def set_hf_off(self):
        self.device.hf_on = False
        return "<ack"

    @add_terminator()
    def set_runmode_on(self):
        self.device.running = True
        return "<ack"

    @add_terminator()
    def set_runmode_off(self):
        self.device.running = False
        return "<ack"

    @add_terminator()
    def get_runmode(self):
        return "<{}".format("on" if self.device.running else "off")

    @add_terminator()
    def get_psu_control_mode(self):
        return "<{}".format("remote" if self.device.remote_mode else "local")

    @add_terminator()
    def get_psu_power(self):
        return "<{}".format("on" if self.device.power_supply_on else "off")

    @add_terminator()
    def get_fan_power(self):
        return "<{}".format("on" if self.device.power_supply_fan_on else "off")

    @add_terminator()
    def get_hf_power(self):
        return "<{}".format("on" if self.device.hf_on else "off")
