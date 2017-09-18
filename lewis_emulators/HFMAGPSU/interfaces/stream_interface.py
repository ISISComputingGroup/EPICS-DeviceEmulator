from lewis.adapters.stream import StreamAdapter
from lewis_emulators.utils.command_builder import CmdBuilder
from datetime import datetime


class HFMAGPSUStreamInterface(StreamAdapter):


    # terminators set to ascii ETX
    in_terminator = "\r\n"
    out_terminator = "\r\n"

    commands = {
        CmdBuilder("read_direction").escape("GET SIGN").build(),
        CmdBuilder("read_output_mode").escape("T").build(),
        CmdBuilder("read_output").escape("GET O").build(),
        CmdBuilder("read_ramp_target").escape("RAMP").build(),
        CmdBuilder("read_heater_status").escape("HEATER").build(),
        CmdBuilder("read_max_target").escape("GET MAX").build(),
        CmdBuilder("read_mid_target").escape("GET MID").build(),
        CmdBuilder("read_ramp_rate").escape("GET RATE").build(),
        CmdBuilder("read_limit").escape("H V").build(),
        CmdBuilder("read_pause").escape("P").build(),
        CmdBuilder("read_heater_value").escape("GET H").build(),

        CmdBuilder("write_direction").escape("D ").arg("-|0|\+").build(),
        CmdBuilder("write_output_mode").escape("T ").arg("AMPS|TESLA").build(),
        CmdBuilder("write_ramp_target").escape("RAMP ").arg("ZERO|MID|MAX").build(),
        CmdBuilder("write_heater_status").escape("H ").arg("OFF|ON").build(),
        CmdBuilder("write_pause").escape("P ").arg("OFF|ON").build(),
        CmdBuilder("write_heater_value").escape("S H ").float().build(),
        CmdBuilder("write_max_target").escape("SET MAX ").float().build(),
        CmdBuilder("write_mid_target").escape("SET MID ").float().build(),
        CmdBuilder("write_ramp_rate").escape("SET RAMP ").float().build(),
        CmdBuilder("write_limit").escape("S L ").float().build()
    }

    def _create_log_message(self, pv, value):
        current_time = datetime.now().strftime('%H:%M:%S')
        self._device.log_message = "{} {}: {}".format(current_time, pv, value)


    def handle_error(self, request, error):
        self.log.error("Error occurred at " + repr(request) + ": " + repr(error))
        print("Error occurred at " + repr(request) + ": " + repr(error))

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
        return "HH.MM.SS CURRENT DIRECTION: {}".format(self._device.direction)

    def write_direction(self, direction):
        self._device.direction = direction
        self._create_log_message("DIRECTION", str(direction))
        return self._device.log_message

    def read_output_mode(self):
        mode = "AMPS"
        if self._device.is_output_mode_tesla:
            mode = "TESLA"
        return "HH.MM.SS UNITS: {}".format(mode)

    def read_output(self):
        # If target is + or - the current output, we are ramping up or down
        # new output = current output +/- ramp rate
        if not self._device.is_paused:
            target = self._get_ramp_target_value()
            if target >= self._device.output:
                self._device.output += self._device.ramp_rate
            elif target < :
                self._device.output -= self._device.ramp_rate
        mode = self._get_output_mode_string()

        return "HH.MM.SS OUTPUT: {} {} AT {} VOLTS".format(self._device.output, mode, self._device.heater_value)

    def write_output_mode(self, output_mode):
        if output_mode == "TESLA":
            self._device.is_output_mode_tesla = True
            self._create_log_message("OUTPUT MODE", output_mode)
        elif output_mode == "AMPS":
            self._device.is_output_mode_tesla = False
            self._create_log_message("OUTPUT MODE", output_mode)
        else:
            raise AssertionError("Invalid arguments sent")
        return self._device.log_message

    def read_ramp_target(self):
        return "HH:MM:SS RAMP TARGET: {}".format(self._device.ramp_target)

    def write_ramp_target(self, ramp_target):
        self._device.ramp_target = ramp_target
        self._create_log_message("RAMP TARGET", ramp_target)
        return self._device.log_message

    def read_ramp_rate(self):
        return "HH:MM:SS RAMP RATE {} A/SEC".format(self._device.ramp_rate)

    def write_ramp_rate(self, ramp_rate):
        self._device.ramp_rate = ramp_rate
        self._create_log_message("RAMP RATE", ramp_rate)
        return self._device.log_message

    def read_heater_status(self):
        heater_value = "OFF"
        if self._device.heater_value:
            heater_value = "ON"
        return "HH:MM:SS HEATER STATUS: {}".format(heater_value)

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
        return "HH:MM:SS PAUSE STATUS: {}".format(paused)

    def write_pause(self, paused):
        mode = self._get_output_mode_string()
        target = self._get_ramp_target_value()
        if paused == "ON":
            self._device.is_paused = True
            output = "HOLDING ON PAUSE AT {} {}".format(self._device.output, mode)
            self._create_log_message("RAMP STATUS", output)
        elif paused == "OFF":
            self._device.is_paused = False
            output = "RAMPING FROM {} TO {} {} AT A/SEC".format(self._device.output,
                                                                target, mode,
                                                                self._device.ramp_rate)
            self._create_log_message("RAMP STATUS", output)
        else:
            raise AssertionError("Invalid arguments sent")

        return self._device.log_message

    def read_heater_value(self):
        return "HH:MM:SS HEATER OUTPUT: {} VOLTS".format(self._device.heater_value)

    def write_heater_value(self, heater_value):
        self._device.heater_value = heater_value
        self._create_log_message("HEATER OUTPUT", heater_value)
        return self._device.log_message

    def read_max_target(self):
        mode = self._get_output_mode_string()
        return "HH:MM:SS MAX SETTING: {} {}".format(self._device.max_target, mode)


    def write_max_target(self, max_target):
        self._device.max_target = max_target
        self._create_log_message("MAX SETTING", max_target)
        return self._device.log_message

    def read_mid_target(self):
        mode = self._get_output_mode_string()
        return "HH:MM:SS MID SETTING: {} {}".format(self._device.mid_target, mode)

    def write_mid_target(self, mid_target):
        self._device.mid_target = mid_target
        self._create_log_message("MID SETTING", mid_target)
        return self._device.log_message

    def read_limit(self):
        return "HH:MM:SS VOLTAGE LIMIT: {} VOLTS".format(self._device.limit)

    def write_limit(self, limit):
        self._device.limit = limit
        self._create_log_message("VOLTAGE LIMIT", limit)
        return self._device.log_message
