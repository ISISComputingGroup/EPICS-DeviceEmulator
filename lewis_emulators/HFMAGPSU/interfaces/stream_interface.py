from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder
from datetime import datetime


class HFMAGPSUStreamInterface(StreamInterface):

    in_terminator = "\r\n"
    out_terminator = chr(19)

    commands = {
        CmdBuilder("read_direction").escape("GET SIGN").build(),
        CmdBuilder("read_output_mode").escape("T").build(),
        CmdBuilder("read_output").escape("GET O").build(),
        CmdBuilder("read_heater_status").escape("HEATER").build(),
        CmdBuilder("read_max_target").escape("GET MAX").build(),
        CmdBuilder("read_mid_target").escape("GET MID").build(),
        CmdBuilder("read_ramp_rate").escape("GET RATE").build(),
        CmdBuilder("read_limit").escape("GET VL").build(),
        CmdBuilder("read_pause").escape("P").build(),
        CmdBuilder("read_heater_value").escape("GET H").build(),
        CmdBuilder("read_constant").escape("GET TPA").build(),

        CmdBuilder("write_direction").escape("D ").arg("0|-|\+").build(),
        CmdBuilder("write_output_mode").escape("T ").arg("OFF|ON").build(),
        CmdBuilder("write_ramp_target").escape("RAMP ").arg("ZERO|MID|MAX").build(),
        CmdBuilder("write_heater_status").escape("H ").arg("OFF|ON").build(),
        CmdBuilder("write_pause").escape("P ").arg("OFF|ON").build(),
        CmdBuilder("write_heater_value").escape("S H ").float().build(),
        CmdBuilder("write_max_target").escape("SET MAX ").float().build(),
        CmdBuilder("write_mid_target").escape("SET MID ").float().build(),
        CmdBuilder("write_ramp_rate").escape("SET RAMP ").float().build(),
        CmdBuilder("write_limit").escape("S L ").float().build(),
        CmdBuilder("write_constant").escape("SET TPA ").float().build()
    }

    def _create_log_message(self, pv, value, suffix=""):
        current_time = datetime.now().strftime('%H:%M:%S')
        self._device.log_message = "{} {}: {} {}".format(current_time, pv, value, suffix)

    def handle_error(self, request, error):
        self.log.error("Error occurred at {}: {}".format(request, error))
        print("Error occurred at {}: {}".format(request, error))

    def _get_output_mode_string(self):
        if self._device.is_output_mode_tesla:
            return "TESLA"
        else:
            return "AMPS"

    def _get_ramp_target_value(self):
        target = 0
        if self._device.ramp_target == "MID":
            target = self._device.mid_target
        elif self._device.ramp_target == "MAX":
            target = self._device.max_target
        return target

    def read_direction(self):
        dir = self._device.direction
        if dir == "+":
            dir_string = "POSITIVE"
        elif dir == "-":
            dir_string = "NEGATIVE"
        elif dir == "0":
            dir_string = "ZERO";
        return "CURRENT DIRECTION: {}\r\n".format(dir_string)

    def write_direction(self, direction):
        self._device.direction = direction
        self._create_log_message("DIRECTION", str(direction))
        return self._device.log_message

    def read_output_mode(self):
        mode = "AMPS"
        if self._device.is_output_mode_tesla:
            mode = "TESLA"
        return "........ UNITS: {}\r\n".format(mode)

    def read_output(self):
        # If target is + or - the current output, we are ramping up or down
        # new output = current output +/- ramp rate
        mode = self._get_output_mode_string()
        return "OUTPUT: {} {} AT {} VOLTS \r\n".format(self._device.output, mode, self._device.heater_value)

    def write_output_mode(self, output_mode):
        # Convert values if output mode is changing between amps(OFF) / tesla(ON)
        constant = self._device.constant
        if output_mode == "ON":
            if not self._device.is_output_mode_tesla:
                self._device.output *= constant
                self._device.max_target *= constant
                self._device.mid_target *= constant
                self._device.is_output_mode_tesla = True
                self._create_log_message("OUTPUT MODE", output_mode)
        elif output_mode == "OFF":
            if constant == 0:
                self._device.error_message = "------> No field constant has been entered"
            else:
                if self._device.is_output_mode_tesla:
                    self._device.output /= constant
                    self._device.max_target /= constant
                    self._device.mid_target /= constant
                    self._device.is_output_mode_tesla = False
                    self._create_log_message("OUTPUT MODE", output_mode)
        else:
            raise AssertionError("Invalid arguments sent")
        return self._device.log_message

    def read_ramp_target(self):
        return "........ RAMP TARGET: {}\r\n".format(self._device.ramp_target)

    def write_ramp_target(self, ramp_target):
        self._device.ramp_target = ramp_target
        self._create_log_message("RAMP TARGET", ramp_target, suffix="A/SEC")
        return self._device.log_message

    def read_ramp_rate(self):
        return "........ RAMP RATE: {} A/SEC\r\n".format(self._device.ramp_rate)

    def write_ramp_rate(self, ramp_rate):
        self._device.ramp_rate = ramp_rate
        self._create_log_message("RAMP RATE", ramp_rate, suffix="A/SEC\r\n")
        return self._device.log_message

    def read_heater_status(self):
        heater_value = "OFF"
        if self._device.is_heater_on:
            heater_value = "ON"
            return "........ HEATER STATUS: {}\r\n".format(heater_value)
        else:
            if self._device.is_output_mode_tesla:
                mode = "TESLA"
            else:
                mode = "AMPS"
            #return "........ HEATER STATUS: {} AT {} {}".format(heater_value, self._device.output, mode)
            return "........ HEATER STATUS: {}\r\n".format(mode)

    def write_heater_status(self, heater_status):
        if heater_status == "ON":
            self._device.is_heater_on = True
            self._create_log_message("HEATER STATUS", heater_status)
        elif heater_status == "OFF":
            self._device.is_heater_on = False
            self._create_log_message("HEATER STATUS", heater_status)
        else:
            raise AssertionError("Invalid arguments sent")
        return self._device.log_message

    def read_pause(self):
        paused = "OFF"
        if self._device.is_paused:
            paused = "ON"
        return "........ PAUSE STATUS: {}\r\n".format(paused)

    def write_pause(self, paused):
        mode = self._get_output_mode_string()
        target = self._get_ramp_target_value()
        rate = self._device.ramp_rate
        output = "HOLDING ON PAUSE AT {} {}".format(self._device.output, mode)
        if paused == "ON":
            self._device.is_paused = True
            self._create_log_message("RAMP STATUS", output)
        elif paused == "OFF":
            self._device.is_paused = False
            ramp_complete = abs(float(self._device.output) - float(target)) < 0.00001
            if ramp_complete:
                self._create_log_message("RAMP STATUS", output)
            else:
                output = "RAMPING FROM {:.6} TO {:.6} {} AT {:.6} A/SEC".format(self._device.output,
                                                                    target, mode, rate)
                self._create_log_message("RAMP STATUS", output)
        else:
            raise AssertionError("Invalid arguments sent")

        return self._device.log_message

    def read_heater_value(self):
        return "........ HEATER OUTPUT: {} VOLTS\r\n".format(self._device.heater_value)

    def write_heater_value(self, heater_value):
        self._device.heater_value = heater_value
        self._create_log_message("HEATER OUTPUT", heater_value)
        return self._device.log_message

    def read_max_target(self):
        mode = self._get_output_mode_string()
        return "........ MAX SETTING: {:.4} {}\r\n".format(self._device.max_target, mode)

    def write_max_target(self, max_target):
        self._device.max_target = max_target
        units = self._get_output_mode_string()
        self._create_log_message("MAX SETTING", max_target,  suffix=units)
        return self._device.log_message

    def read_mid_target(self):
        mode = self._get_output_mode_string()
        return "........ MID SETTING: {:.4} {}\r\n".format(self._device.mid_target, mode)

    def write_mid_target(self, mid_target):
        self._device.mid_target = mid_target
        units = self._get_output_mode_string()
        self._create_log_message("MID SETTING", mid_target, suffix="{}\r\n".format(units))
        return self._device.log_message

    def read_limit(self):
        return "........ VOLTAGE LIMIT: {} VOLTS\r\n".format(self._device.limit)

    def write_limit(self, limit):
        self._device.limit = limit
        self._create_log_message("VOLTAGE LIMIT", limit)
        return self._device.log_message

    def read_constant(self):
        return "........ FIELD CONSTANT: {:.7} T/A\r\n".format(self._device.constant)

    def write_constant(self, constant):
        self._device.constant = constant
        self._create_log_message("FIELD CONSTANT", constant, suffix="T/A")
        return self._device.log_message
