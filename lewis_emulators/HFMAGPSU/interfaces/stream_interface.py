from lewis.adapters.stream import StreamAdapter
from lewis_emulators.utils.command_builder import CmdBuilder

class HFMAGPSUStreamInterface(StreamAdapter):

    # terminators set to ascii ETX
    in_terminator = chr(3)
    out_terminator = ""



    commands = {
        CmdBuilder("read_direction").escape("GETSIGN").build(),
        CmdBuilder("read_output_mode").escape("GETO").build(),
        CmdBuilder("read_ramp_target").escape("RS").build(),
        CmdBuilder("read_heater_status").escape("H").build(),
        CmdBuilder("read_heater_value").escape("GETVL").build(),
        CmdBuilder("read_max_target").escape("GETMAX").build(),
        CmdBuilder("read_mid_target").escape("GETMID").build(),
        CmdBuilder("read_ramp_rate").escape("R").build(),
        CmdBuilder("read_limit").escape("HV").build(),
        CmdBuilder("read_update").escape("U").build(),

        CmdBuilder("write_direction").escape("D").arg("0|-|\+").build(), # '+' is special character
        CmdBuilder("write_output_mode").escape("T ").arg("OFF|ON").build(),
        CmdBuilder("write_ramp_target").escape("RAMP ").arg("0|%|!").build(),
        CmdBuilder("write_heater_status").escape("H ").arg("OFF|ON").build(),
        CmdBuilder("write_heater_value").escape("SH ").float().build(),
        CmdBuilder("write_max_target").escape("SET MAX").float().build(),
        CmdBuilder("write_mid_target").escape("SET MID").float().build(),
        CmdBuilder("write_ramp_rate").escape("SET RAMP").float().build(),
        CmdBuilder("write_limit").escape("SL").float().build(),
    }

    def handle_error(self, request, error):
        self.log.error("Beep boop. Error occurred at " + repr(request) + ": " + repr(error))
        print("Beep boop. Error occurred at " + repr(request) + ": " + repr(error))

    def read_direction(self):
        return self._device.direction

    def read_output_mode(self):
        return self._device.outputMode

    def read_ramp_target(self):
        return self._device.rampTarget

    def read_ramp_rate(self):
        return self._device.rampRate

    def read_heater_status(self):
        return self._device.heaterStatus

    def read_heater_value(self):
        return self._device.heaterValue

    def read_max_target(self):
        return self._device.maxTarget

    def read_mid_target(self):
        return self._device.midTarget

    def read_limit(self):
        return self._limit

    def read_update(self):
        return self._update

    def write_max_target(self, mt):
        self._device.maxTarget = mt
        return "MAX TARGET SET TO: " + mt

    def write_mid_target(self, mt):
        self._device.midTarget = mt
        return "MID TARGET SET TO: " + mt

    def write_ramp_rate(self, rr):
        self._device.rampRate = rr
        return "RAMP RATE SET TO: " + rr

    def write_direction(self, d):
        self._device.direction = d
        return "DIRECTION SET TO: " + d

    def write_ramp_target(self, rt):
        self._device.rampTarget = rt
        return "RAMP TARGET SET TO: " + rt

    def write_heater_status(self, hs):
        self._device.heaterStatus = hs
        return "HEATER STATUS SET TO: " + hs

    def write_heater_value(self, hv):
        self._device.heaterValue = hv
        return "HEATER VALUE SET TO: " + hv + " VOLTS"

    def write_output_mode(self, om):
        self._device.outputMode = om
        return "OUTPUT MODE SET TO: " + om

    def write_limit(self, l):
        self._device.limit = l
        return "LIMIT SET TO: " + l + " VOLTS"
