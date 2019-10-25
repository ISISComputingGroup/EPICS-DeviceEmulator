from lewis.adapters.stream import StreamInterface, Cmd
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis_emulators.utils.constants import ACK, ENQ


@has_log
class IceFridgeStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("set_auto_temp_setpoint").escape("AUTO TSET=").float().eos().build(),
        CmdBuilder("get_auto_temp_set_RBV").escape("AUTO TSET?").eos().build(),
        CmdBuilder("get_auto_temp_set_RBV").escape("AUTO TEMP?").eos().build(),

        CmdBuilder("set_manual_temp_setpoint").escape("MANUAL TSET=").float().eos().build(),
        CmdBuilder("get_manual_temp_set_RBV").escape("MANUAL TSET?").eos().build(),
        CmdBuilder("get_manual_temp_set_RBV").escape("MANUAL TEMP?").eos().build(),

        CmdBuilder("get_cryo_temps").escape("CRYO-TEMPS?").eos().build(),

        CmdBuilder("set_loop_temp_setpoint").escape("CRYO-TSET=").int().escape(",").float().eos().build(),
        CmdBuilder("get_loop_temp").escape("CRYO-TSET").int().escape("?").eos().build(),

        CmdBuilder("set_loop_proportional_setpoint").escape("CRYO-P=").int().escape(",").float().eos().build(),
        CmdBuilder("get_loop_proportional").escape("CRYO-P").int().escape("?").eos().build(),

        CmdBuilder("set_loop_integral_setpoint").escape("CRYO-I=").int().escape(",").float().eos().build(),
        CmdBuilder("get_loop_integral").escape("CRYO-I").int().escape("?").eos().build(),

        CmdBuilder("set_loop_derivative_setpoint").escape("CRYO-D=").int().escape(",").float().eos().build(),
        CmdBuilder("get_loop_derivative").escape("CRYO-D").int().escape("?").eos().build(),

        CmdBuilder("set_loop_ramp_rate_setpoint").escape("CRYO-RAMP=").int().escape(",").float().eos().build(),
        CmdBuilder("get_loop_ramp_rate").escape("CRYO-RAMP").int().escape("?").eos().build(),

        CmdBuilder("get_mc_cernox").escape("LS-DIRECT-READ=RDGK? 4").eos().build()
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        """
        Prints and logs an error message if a command is not recognised.

        Args:
            request : Request.
            error: The error that has occurred.
        Returns:
            String: The error string.
        """
        err_string = "command was: \"{}\", error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    def set_auto_temp_setpoint(self, temp_setpoint):
        self._device.auto_temp_setpoint = temp_setpoint

    def get_auto_temp_set_RBV(self):
        return self._device.auto_temp_setpoint

    def set_manual_temp_setpoint(self, temp_setpoint):
        self._device.manual_temp_setpoint = temp_setpoint

    def get_manual_temp_set_RBV(self):
        return self._device.manual_temp_setpoint

    def get_cryo_temps(self):
        return "CRYO-TEMPS={},{},{},{}".format(self._device.vti_temp1, self._device.vti_temp2, self._device.vti_temp3,
                                               self._device.vti_temp4)

    def set_loop_temp_setpoint(self, loop_num, temp_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_temp_setpoint = temp_setpoint

    def get_loop_temp(self, loop_num):
        return "CRYO-TSET{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_temp_setpoint)

    def set_loop_proportional_setpoint(self, loop_num, proportional_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_proportional = proportional_setpoint

    def get_loop_proportional(self, loop_num):
        return "CRYO-P{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_proportional)

    def set_loop_integral_setpoint(self, loop_num, integral_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_integral = integral_setpoint

    def get_loop_integral(self, loop_num):
        return "CRYO-I{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_integral)

    def set_loop_derivative_setpoint(self, loop_num, derivative_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_derivative = derivative_setpoint

    def get_loop_derivative(self, loop_num):
        return "CRYO-D{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_derivative)

    def set_loop_ramp_rate_setpoint(self, loop_num, ramp_rate_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_ramp_rate = ramp_rate_setpoint

    def get_loop_ramp_rate(self, loop_num):
        return "CRYO-RAMP{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_ramp_rate)

    def get_mc_cernox(self):
        return self._device.lakeshore_mc_cernox
