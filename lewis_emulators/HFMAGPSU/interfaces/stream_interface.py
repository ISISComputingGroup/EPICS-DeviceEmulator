from lewis.adapters.stream import StreamAdapter
from lewis_emulators.utils.command_builder import CmdBuilder

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

    def handle_error(self, request, error):
        self.log.error("Beep boop. Error occurred at " + repr(request) + ": " + repr(error))
        print("Beep boop. Error occurred at " + repr(request) + ": " + repr(error))

    def read_direction(self):
        return self._device.direction

    def write_direction(self, d):
        self._device.direction = d
        self._device.logMessage = "HH:MM:SS DIRECTION: [" + str(d) + "]"
        return self._device.logMessage

    def read_output_mode(self):
        return "TESLA" if self._device.isOutputModeTesla else "AMPS"

    def write_output_mode(self, om):
        if om == "TESLA":
            self._device.isOutputModeTesla = True
        else:
            self._device.isOutputModeTesla = False
        self._device.logMessage = "HH:MM:SS UNITS: [" + str(om) + "]"
        return self._device.logMessage

    def read_ramp_target(self):
        return self._device.rampTarget

    def write_ramp_target(self, rt):
        self._device.rampTarget = rt
        self._device.logMessage = "HH:MM:SS RAMP TARGET: [" + str(rt) + "]"
        return self._device.logMessage

    def read_ramp_rate(self):
        return self._device.rampRate

    def write_ramp_rate(self, rr):
        self._device.rampRate = rr
        self._device.logMessage = "HH:MM:SS RAMP RATE: [" + str(rr) + "]"
        return self._device.logMessage

    def read_heater_status(self):
        return "ON" if self._device.isHeaterOn else "OFF"

    def write_heater_status(self, hs):
        if hs == "ON":
            self._device.isHeaterOn = True
        else:
            self._device.isHeaterOn = False
        self._device.logMessage = "HH:MM:SS HEATER STATUS: [" + str(hs) + "]"
        return self._device.logMessage

    def read_pause(self):
        return "ON" if self._device.isPaused else "OFF"

    def write_pause(self, paused):
        if paused == "ON":
            self._device.isPaused = True
        else:
            self._device.isPaused = False
        self._device.logMessage = "HH:MM:SS PAUSE STATUS: [" + str(paused) + "]"
        return self._device.logMessage

    def read_heater_value(self):
        return self._device.heaterValue

    def write_heater_value(self, hv):
        self._device.heaterValue = hv
        self._device.logMessage = "HH:MM:SS HEATER OUTPUT: [" + str(hv) + "]"
        return self._device.logMessage

    def read_max_target(self):
        return self._device.maxTarget

    def write_max_target(self, mt):
        self._device.maxTarget = mt
        self._device.logMessage = "HH:MM:SS MAX SETTING: [" + str(mt) + "]"
        return self._device.logMessage

    def read_mid_target(self):
        return self._device.midTarget

    def write_mid_target(self, mt):
        self._device.midTarget = mt
        self._device.logMessage = "HH:MM:SS MID SETTING: [" + str(mt) + "]"
        return self._device.logMessage

    def read_limit(self):
        return self._device.limit

    def write_limit(self, l):
        self._device.limit = l
        self._device.logMessage = "HH:MM:SS VOLTAGE LIMIT: [" + str(l) + "]"
        return self._device.logMessage
