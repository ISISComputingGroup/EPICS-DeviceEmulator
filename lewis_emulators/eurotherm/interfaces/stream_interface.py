from lewis.adapters.stream import StreamAdapter
from lewis_emulators.utils.command_builder import CmdBuilder


class EurothermStreamInterface(StreamAdapter):
    """
    Stream interface for the serial port
    """

    commands = {
        CmdBuilder("get_current_temperature").eot().escape("0011PV").enq().build(),
        CmdBuilder("get_ramp_setpoint").eot().escape("0011SP").enq().build(),
        CmdBuilder("set_ramp_setpoint", arg_sep="").eot().escape("0011").stx().escape("SL").float().etx().any().build(),
    }

    # The real Eurotherm uses timeouts instead of terminators to assess when a command is finished. To make this work
    # with the emulator we manually added terminators via asyn commands to the device. Lewis will be able to handle this
    # natively in future versions. See: https://github.com/DMSC-Instrument-Data/lewis/pull/262
    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def get_current_temperature(self):
        """
        Get the current temperature of the device.

        Returns: the current temperature formatted like the Eurotherm protocol.
        """
        return "\x02PV{}".format(self._device.current_temperature)

    def get_ramp_setpoint(self):
        """
        Get the set point temperature.

        Returns: the current set point temperature formatted like the Eurotherm protocol.
        """
        return "\x02SP{}".format(self._device.ramp_setpoint_temperature)

    def set_ramp_setpoint(self, temperature, _):
        """
        Set the set point temperature.

        Args:
            temperature: the temperature to set the setpoint to.
            _: unused argument captured by the command.

        """
        self._device.ramp_setpoint_temperature = temperature
