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
        CmdBuilder("set_loop1_temp_setpoint").escape("CRYO-TSET=1,").float().eos().build(),
        CmdBuilder("get_loop1_temp_setpoint").escape("CRYO-TSET1?").eos().build(),
        CmdBuilder("set_loop2_temp_setpoint").escape("CRYO-TSET=2,").float().eos().build(),
        CmdBuilder("get_loop2_temp_setpoint").escape("CRYO-TSET2?").eos().build()
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

    def set_loop1_temp_setpoint(self, temp_setpoint):
        self._device.vti_loop1_temp_setpoint = temp_setpoint

    def get_loop1_temp_setpoint(self):
        return "CRYO-TSET1={}".format(self._device.vti_loop1_temp_setpoint)

    def set_loop2_temp_setpoint(self, temp_setpoint):
        self._device.vti_loop2_temp_setpoint = temp_setpoint

    def get_loop2_temp_setpoint(self):
        return "CRYO-TSET2={}".format(self._device.vti_loop2_temp_setpoint)
