import six
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
import abc

from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


def needs_remote_mode(func):
    @six.wraps(func)
    def _wrapper(self, *args, **kwargs):
        if not self._device.remote_comms_enabled:
            raise ValueError("Not in remote mode")
        return func(self, *args, **kwargs)
    return _wrapper


@has_log
@six.add_metaclass(abc.ABCMeta)
class KepcoStreamInterface(object):

    in_terminator = "\r\n"
    out_terminator = "\r\n"

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
        CmdBuilder("get_IDN").escape("*IDN?").build(),
        CmdBuilder("set_control_mode").escape("SYST:REM ").arg("0|1").build(),
        CmdBuilder("reset").escape("*RST").build()
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
    @needs_remote_mode
    def write_voltage(self, voltage):
        self._device.setpoint_voltage = voltage

    @if_connected
    @needs_remote_mode
    def write_current(self, current):
        self._device.setpoint_current = current

    @if_connected
    def read_setpoint_voltage(self):
        return "{0}".format(self._device.setpoint_voltage)

    @if_connected
    def read_setpoint_current(self):
        return "{0}".format(self._device.setpoint_current)

    @if_connected
    @needs_remote_mode
    def set_output_mode(self, mode):
        self._device.output_mode = mode

    @if_connected
    def read_output_mode(self):
        return "{0}".format(self._device.output_mode)

    @if_connected
    @needs_remote_mode
    def set_output_status(self, status):
        self._device.output_status = status

    @if_connected
    def read_output_status(self):
        return "{0}".format(self._device.output_status)

    @if_connected
    def get_IDN(self):
        return "{0}".format(self._device.idn)

    @if_connected
    def set_control_mode(self, mode):
        raise NotImplementedError

    @if_connected
    def reset(self):
        self._device.reset()
