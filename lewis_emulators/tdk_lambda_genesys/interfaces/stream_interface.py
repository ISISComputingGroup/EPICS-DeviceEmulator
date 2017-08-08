from lewis.adapters.stream import StreamAdapter, Cmd
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder


class TDKLambdaGenesysStreamInterface(StreamAdapter):
    commands = {
        CmdBuilder("write_voltage").escape("PV ").float().build(),
        CmdBuilder("read_setpoint_voltage").escape("PV?").build(),
        CmdBuilder("read_voltage").escape("MV?").build(),
        CmdBuilder("write_current").escape("PC ").float().build(),
        CmdBuilder("read_setpoint_current").escape("PC?").build(),
        CmdBuilder("read_current").escape("MC?").build(),
        CmdBuilder("remote").escape("RMT 1").build(),
        CmdBuilder("write_power").escape("OUT ").arg("[OFF|ON]").build(),
        CmdBuilder("read_power").escape("OUT?").build(),
    }

    in_terminator = "\r"
    out_terminator = "\r"

    def handle_error(self,request, error):
        self.log.error("Beep boop. Error occurred at " + repr(request) + ": " + repr(error))
        print("Beep boop. Error occurred at " + repr(request) + ": " + repr(error))

    def read_voltage(self):
        return self._device.voltage

    def read_setpoint_voltage(self):
        return self._device.setpoint_voltage

    def write_voltage(self, v):
        self._device.setpoint_voltage = v
        return "VOLTAGE SET TO: " + v

    def read_current(self):
        return self._device.current

    def read_setpoint_current(self):
        return self._device.setpoint_current

    def write_current(self, c):
        self._device.setpoint_current = c
        return "VOLTAGE SET TO: " + c

    def read_power(self):
        return self._device.powerstate

    def write_power(self, p):
        self._device.powerstate = p
        return "POWER SET TO " + p

    def remote(self):
        # We can ignore this command
        pass

