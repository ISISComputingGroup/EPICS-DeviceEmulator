from lewis.adapters.stream import StreamAdapter
from utils.command_builder import CmdBuilder
from lewis.core.logging import has_log

@has_log
class KepcoStreamInterface(StreamAdapter):

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

    def read_actual_voltage(self):
        return "{0}".format(self._device.voltage)

    def read_actual_current(self):
        return "{0}".format(self._device.current)

    def write_voltage(self, voltage):
        self._device.setpoint_voltage = voltage

    def write_current(self, current):
        self._device.setpoint_current = current

    def read_setpoint_voltage(self):
        return "{0}".format(self._device.setpoint_voltage)

    def read_setpoint_current(self):
        return "{0}".format(self._device.setpoint_current)

    def set_output_mode(self, mode):
        self._device.output_mode = mode

    def read_output_mode(self):
        return "{0}".format(self._device.output_mode)

    def set_output_status(self, status):
        self._device.output_status = status

    def read_output_status(self):
        return "{0}".format(self._device.output_status)

    def get_IDN(self):
        return "{0}".format(self._device.idn)
