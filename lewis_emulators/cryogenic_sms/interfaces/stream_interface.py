from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from datetime import datetime
from ..utils import RampTarget


@has_log
class CRYOSMSStreamInterface(StreamInterface):

    in_terminator = "\r\n"
    out_terminator = chr(19)

    def __init__(self):
        re_set = " *S(?:ET)* *"  # Set regex for shorthand or longhand with 0 or more leading and trailing spaces
        re_get = " *G(?:ET)* *"  # Get regex
        self.commands = {
            # Get commands
            CmdBuilder(self.read_direction).regex(re_get).regex("S(?:IGN)*").spaces().eos().build(),
            CmdBuilder(self.read_output_mode).spaces().regex("T(?:ESLA)*").spaces().eos().build(),
            CmdBuilder(self.read_output).regex(re_get).regex("O(?:UTPUT)*").spaces().eos().build(),
            CmdBuilder(self.read_ramp_status).spaces().regex("R(?:AMP)*").spaces().regex("S(?:TATUS)*").spaces().eos()
                                             .build(),
            CmdBuilder(self.read_heater_status).spaces().escape("H(?:EATER)*").spaces().eos().build(),
            CmdBuilder(self.read_max_target).regex(re_get).choice("MAX", "!").spaces().eos().build(),
            CmdBuilder(self.read_mid_target).regex(re_get).choice("MID", "%").spaces().eos().build(),
            CmdBuilder(self.read_ramp_rate).regex(re_get).regex("R(?:ATE)*").spaces().eos().build(),
            CmdBuilder(self.read_limit).regex(re_get).regex("V(?:L)*").spaces().eos().build(),
            CmdBuilder(self.read_pause).spaces().regex("P(?:AUSE)*").spaces().eos().build(),
            CmdBuilder(self.read_heater_value).regex(re_get).regex("H(?:V)*").spaces().eos().build(),
            CmdBuilder(self.read_constant).regex(re_get).regex("T(?:PA)").spaces().eos().build(),

            # Set commands
            CmdBuilder(self.write_direction).spaces().regex("D(?:IRECTION)*").spaces().arg("0|-|\+").spaces().eos()
                                            .build(),
            CmdBuilder(self.write_output_mode).spaces().regex("T(?:ESLA)*").spaces().arg("OFF|ON|0|1").spaces().eos()
                                              .build(),
            CmdBuilder(self.write_ramp_target).spaces().regex("R(?:AMP)*").spaces().arg("ZERO|MID|MAX|0|%|!")
                                              .spaces().eos().build(),
            CmdBuilder(self.write_heater_status).spaces().regex("H(?:EATER)*").spaces().arg("OFF|ON|1|0").spaces()
                                                .eos().build(),
            CmdBuilder(self.write_pause).spaces().regex("P(?:AUSE)*").spaces().arg("OFF|ON|0|1").spaces().eos().build(),
            CmdBuilder(self.write_heater_value).regex(re_set).escape("H(?:EATER)*").spaces().float().spaces().eos()
                                               .build(),
            CmdBuilder(self.write_max_target).regex(re_set).choice("MAX", "!").spaces().float().spaces().eos().build(),
            CmdBuilder(self.write_mid_target).regex(re_set).choice("MID", "%").spaces().float().spaces().eos().build(),
            CmdBuilder(self.write_ramp_rate).regex(re_set).regex("R(?:AMP)*").spaces().float().spaces().eos().build(),
            CmdBuilder(self.write_limit).regex(re_set).regex("L(?:IMIT)*").spaces().float().spaces().eos().build(),
            CmdBuilder(self.write_constant).regex(re_set).regex("T(?:PA)*").spaces().float().spaces().eos().build()
        }

    def _out_message(self, message):
        return "........{}\r\n".format(message)

    def _timestamp(self):
        return datetime.now().strftime('%H:%M:%S')

    def _create_log_message(self, pv, value, suffix=""):
        current_time = self._timestamp()
        self._device.log_message = "{} {}: {}{}\r\n".format(current_time, pv, value, suffix)

    def handle_error(self, request, error):
        self.log.error("Error occurred at {}: {}".format(request, error))

    def _get_output_mode_string(self):
        return "TESLA" if self._device.is_output_mode_tesla else "AMPS"

    def _get_paused_state_str(self):
        return "ON" if self._device.is_paused else "OFF"

    def _get_ramp_target_value(self):
        if self._device.ramp_target.name == "MID":
            return self._device.mid_target
        elif self._device.ramp_target.name == "MAX":
            return self._device.max_target
        elif self._device.ramp_target.name == "ZERO":
            return self._device.zero_target

    def read_direction(self):
        dir_dict = {"+": "POSITIVE", "-": "NEGATIVE", "0": "ZERO"}
        return "CURRENT DIRECTION: {}\r\n".format(dir_dict[self._device.direction])

    def write_direction(self, direction):
        self._device.direction = direction
        return self._out_message("")

    def read_output_mode(self):
        return self._out_message("UNITS: {}".format(self._get_output_mode_string()))

    def read_output(self):
        return "{} OUTPUT: {} {} AT {} VOLTS \r\n".format(self._timestamp(),
                                                          self._device.output,
                                                          self._get_output_mode_string(),
                                                          self._device.heater_value)

    def write_output_mode(self, output_mode):
        # Convert values if output mode is changing between amps(OFF) / tesla(ON)
        constant = self._device.constant
        if output_mode in ["ON", "1"]:
            if not self._device.is_output_mode_tesla:
                self._device.switch_mode("TESLA")
                self._create_log_message("UNITS", "TESLA")
        elif output_mode in ["OFF", "0"]:
            if constant == 0:
                self._device.error_message = "------> No field constant has been entered"
            else:
                if self._device.is_output_mode_tesla:
                    self._device.switch_mode("AMPS")
                    self._create_log_message("UNITS", "AMPS")
        else:
            raise ValueError("Invalid arguments sent")
        return self._device.log_message

    def read_ramp_target(self):
        return self._out_message(" RAMP TARGET: {}".format(self._device.ramp_target.name))

    def read_ramp_status(self):
        output = self._device.output
        status_message = " RAMP STATUS: "
        if self._device.is_paused:
            status_message += "HOLDING ON PAUSE AT {} {}".format(output, self._get_output_mode_string())
        elif self._device.at_target:
            status_message += "HOLDING ON TARGET AT {} {}".format(output, self._get_output_mode_string())
        elif self._device.is_quenched:
            status_message += "QUENCH TRIP AT {} {}".format(output, self._get_output_mode_string())
        elif self._device.is_xtripped:
            status_message += "EXTERNAL TRIP AT {} {}".format(output, self._get_output_mode_string())
        elif not self._device.at_target and not self._device.is_paused:
            status_message += "RAMPING FROM {} TO {} {} AT {:07.5f} A/SEC".format(self._device.prev_target,
                                                                                  self._device.mid_target,
                                                                                  self._get_output_mode_string(),
                                                                                  self._device.ramp_rate)
        else:
            raise ValueError("Didn't match any of the expected conditions")
        return self._out_message(status_message)

    def write_ramp_target(self, ramp_target_str):
        if ramp_target_str in ["0", "ZERO"]:
            ramp_target = RampTarget.ZERO
        elif ramp_target_str in ["%", "MID"]:
            ramp_target = RampTarget.MID
        elif ramp_target_str in ["!", "MAX"]:
            ramp_target = RampTarget.MAX
        else:
            raise ValueError("Invalid arguments sent")
        self._device.ramp_target = ramp_target
        self._device.is_paused = False
        self._create_log_message("RAMP TARGET", ramp_target.name)
        return self._device.log_message

    def read_ramp_rate(self):
        return self._out_message(" RAMP RATE: {} A/SEC".format(self._device.ramp_rate))

    def write_ramp_rate(self, ramp_rate):
        self._device.ramp_rate = ramp_rate
        self._create_log_message("RAMP RATE", ramp_rate, suffix=" A/SEC")
        return self._device.log_message

    def read_heater_status(self):
        heater_value = "ON" if self._device.is_heater_on else "OFF"
        return self._out_message(" HEATER STATUS: {}".format(heater_value))

    def write_heater_status(self, heater_status):
        if heater_status in ["ON", "1"]:
            self._device.is_heater_on = True
        elif heater_status in ["OFF", "0"]:
            self._device.is_heater_on = False
        else:
            raise ValueError("Invalid arguments sent")
        self._create_log_message("........ HEATER STATUS", heater_status)
        return self._device.log_message

    def read_pause(self):
        return self._out_message(" PAUSE STATUS: {}".format(self._get_paused_state_str()))

    def write_pause(self, paused):
        mode = self._get_output_mode_string()
        target = self._get_ramp_target_value()
        rate = self._device.ramp_rate
        output = "HOLDING ON PAUSE AT {} {}".format(self._device.output, mode)
        if paused in ["ON", "1"]:
            self._device.is_paused = True
            self._create_log_message("PAUSE STATUS", output)
        elif paused in ["OFF", "0"]:
            self._device.is_paused = False
            if self._device.check_is_at_target():
                self._create_log_message("RAMP STATUS", output)
            else:
                output = "RAMPING FROM {:.6} TO {:.6} {} AT {:.6} A/SEC".format(self._device.output,
                                                                                target, mode, rate)
                self._create_log_message("RAMP STATUS", output)
        else:
            raise ValueError("Invalid arguments sent")

        return self._out_message(" PAUSE STATUS: {}".format(paused))

    def read_heater_value(self):
        return self._out_message(" HEATER OUTPUT: {} VOLTS".format(self._device.heater_value))

    def write_heater_value(self, heater_value):
        self._device.heater_value = heater_value
        self._create_log_message("HEATER OUTPUT", heater_value, suffix=" VOLTS")
        return self._device.log_message

    def read_max_target(self):
        mode = self._get_output_mode_string()
        return self._out_message(" MAX SETTING: {:.4} {}".format(self._device.max_target, mode))

    def write_max_target(self, max_target):
        self._device.max_target = abs(max_target)  # abs because PSU ignores sign
        units = self._get_output_mode_string()
        self._create_log_message("MAX SETTING", max_target,  suffix=" {}\r\n".format(units))
        return self._device.log_message

    def read_mid_target(self):
        mode = self._get_output_mode_string()
        return self._out_message(" MID SETTING: {:.4} {}".format(self._device.mid_target, mode))

    def write_mid_target(self, mid_target):
        self._device.mid_target = abs(mid_target)  # abs because PSU ignores sign
        units = self._get_output_mode_string()
        self._create_log_message("MID SETTING", mid_target, suffix=" {}".format(units))
        return self._device.log_message

    def read_limit(self):
        return self._out_message(" VOLTAGE LIMIT: {} VOLTS".format(self._device.limit))

    def write_limit(self, limit):
        self._device.limit = limit
        self._create_log_message("VOLTAGE LIMIT", limit, suffix=" VOLTS")
        return self._device.log_message

    def read_constant(self):
        return self._out_message(" FIELD CONSTANT: {:.7} T/A".format(self._device.constant))

    def write_constant(self, constant):
        self._device.constant = constant
        self._create_log_message("FIELD CONSTANT", constant, suffix=" T/A")
        return self._device.log_message
