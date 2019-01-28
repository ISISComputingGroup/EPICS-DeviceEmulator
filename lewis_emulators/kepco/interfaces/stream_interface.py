from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log

from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


@has_log
class KepcoStreamInterface(StreamInterface):

    in_terminator="\r\n"
    out_terminator="\r\n"

    commands = {
        CmdBuilder("write_voltage").escape("VOLT ").float().build(),
        CmdBuilder("read_actual_voltage").escape("MEAS:VOLT?").build(),
        CmdBuilder("read_actual_current").escape("MEAS:CURR?").build(),
        CmdBuilder("write_current").escape("CURR ").float().build(),
        CmdBuilder("read_setpoint_voltage").escape("VOLT?").build(),
        CmdBuilder("read_setpoint_current").escape("CURR?").build(),
        CmdBuilder("set_output_mode").escape("FUNC:MODE ").arg("VOLT|CURR").build(),
        CmdBuilder("read_output_mode").escape("FUNC:MODE?").build(),
        CmdBuilder("read_output_status").escape("OUTP?").build(),
        CmdBuilder("set_output_status").escape("OUTP ").arg("0|1").build(),
        CmdBuilder("get_IDN").escape("*IDN?").build()
    }

    def handle_error(self,request, error):
        self.log.error("An error occurred at request" + repr(request) + ": " + repr(error))
        print("An error occurred at request" + repr(request) + ": " + repr(error))

    @if_connected
    def read_actual_voltage(self):
        return "{0}".format(self._device.voltage)

    @if_connected
    def read_actual_current(self):
        return "{0}".format(self._device.current)

    @if_connected
    def write_voltage(self, voltage):
        self._device.setpoint_voltage = voltage

    @if_connected
    def write_current(self, current):
        self._device.setpoint_current = current

    @if_connected
    def read_setpoint_voltage(self):
        return "{0}".format(self._device.setpoint_voltage)

    @if_connected
    def read_setpoint_current(self):
        return "{0}".format(self._device.setpoint_current)

    @if_connected
    def set_output_mode(self, mode):
        self._device.output_mode = mode

    @if_connected
    def read_output_mode(self):
        return "{0}".format(self._device.output_mode)

    @if_connected
    def set_output_status(self, status):
        self._device.output_status = status

    @if_connected
    def read_output_status(self):
        return "{0}".format(self._device.output_status)

    @if_connected
    def get_IDN(self):
        return "{0}".format(self._device.idn)
