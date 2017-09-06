from lewis.adapters.stream import StreamAdapter
from lewis_emulators.utils.command_builder import CmdBuilder
from datetime import datetime


class HFMAGPSUStreamInterface(StreamAdapter):


    # terminators set to ascii ETX
    in_terminator = "\r\n"
    out_terminator = "\r\n"

    commands = {
        CmdBuilder("read_direction").escape("GET SIGN").build(),
        CmdBuilder("read_output_mode").escape("GET O").build(),
        CmdBuilder("read_ramp_target").escape("R S").build(),
        CmdBuilder("read_heater_status").escape("HEATER").build(),
        CmdBuilder("read_max_target").escape("GET MAX").build(),
        CmdBuilder("read_mid_target").escape("GET MID").build(),
        CmdBuilder("read_ramp_rate").escape("RAMP").build(),
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
        self._device.log_message = "{} {}: [{}]".format(current_time, pv, value)

    def handle_error(self, request, error):
        self.log.error("Error occurred at " + repr(request) + ": " + repr(error))
        print("Error occurred at " + repr(request) + ": " + repr(error))

    def read_direction(self):
        return self._device.direction

    def write_direction(self, direction):
        self._device.direction = direction
        self._create_log_message("DIRECTION", str(direction))
        return self._device.log_message

    def read_output_mode(self):
        return "TESLA" if self._device.is_output_mode_tesla else "AMPS"

    def write_output_mode(self, output_mode):
        if output_mode == "TESLA":
            self._device.is_output_mode_tesla = True
            self._create_log_message("OUTPUT MODE", str(output_mode))
        elif output_mode == "AMPS":
            self._device.is_output_mode_tesla = False
            self._create_log_message("OUTPUT MODE", str(output_mode))
        else:
            raise AssertionError("Invalid arguments sent")
        return self._device.log_message

    def read_ramp_target(self):
        return self._device.ramp_target

    def write_ramp_target(self, ramp_target):
        self._device.ramp_target = ramp_target
        self._create_log_message("RAMP TARGET", str(ramp_target))
        return self._device.log_message

    def read_ramp_rate(self):
        return self._device.ramp_rate

    def write_ramp_rate(self, ramp_rate):
        self._device.ramp_rate = ramp_rate
        self._create_log_message("RAMP RATE", str(ramp_rate))
        return self._device.log_message

    def read_heater_status(self):
        return "ON" if self._device.is_heater_on else "OFF"

    def write_heater_status(self, heater_status):
        if heater_status == "ON":
            self._device.is_heater_on = True
            self._create_log_message("HEATER STATUS", str(heater_status))
        elif heater_status == "OFF":
            self._device.is_heater_on = False
            self._create_log_message("HEATER STATUS", str(heater_status))
        else:
            raise AssertionError("Invalid arguments sent")
        return self._device.log_message

    def read_pause(self):
        return "ON" if self._device.is_paused else "OFF"

    def write_pause(self, paused):
        if paused == "ON":
            self._device.is_paused = True
            self._create_log_message("PAUSE STATUS", str(paused))
        elif paused == "OFF":
            self._device.is_paused = False
            self._create_log_message("PAUSE STATUS", str(paused))
        else:
            raise AssertionError("Invalid arguments sent")

        return self._device.log_message

    def read_heater_value(self):
        return self._device.heater_value

    def write_heater_value(self, heater_value):
        self._device.heater_value = heater_value
        self._create_log_message("HEATER OUTPUT", str(heater_value))
        return self._device.log_message

    def read_max_target(self):
        return self._device.max_target

    def write_max_target(self, max_target):
        self._device.max_target = max_target
        self._create_log_message("MAX SETTING", str(max_target))
        return self._device.log_message

    def read_mid_target(self):
        return self._device.mid_target

    def write_mid_target(self, mid_target):
        self._device.mid_target = mid_target
        self._create_log_message("MID SETTING", str(mid_target))
        return self._device.log_message

    def read_limit(self):
        return self._device.limit

    def write_limit(self, limit):
        self._device.limit = limit
        self._create_log_message("VOLTAGE LIMIT", limit)
        return self._device.log_message
