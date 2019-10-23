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
        CmdBuilder("get_auto_temp_set_RBV").escape("TEMPS?").eos().build(),
        CmdBuilder("")
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