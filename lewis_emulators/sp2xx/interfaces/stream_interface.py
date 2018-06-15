from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.if_connected import if_connected
from ..device import RunStatus


@has_log
class Sp2XXStreamInterface(StreamInterface):
    """
    Stream interface for the serial port.
    """

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("set_run_status").escape("run").eos().build(),
        CmdBuilder("get_run_status").escape("run?").eos().build()
    }

    in_terminator = "\r\n"
    out_terminator = ""

    _return = "\r\n"
    Infusing = "{}>".format(_return)
    Withdrawing = "{}<".format(_return)
    Stopped = "{}:".format(_return)

    def handle_error(self, request, error):
        """
        Prints an error message if a command is not recognised.

        Args:
            request : Request.
            error: The error that has occurred.
        Returns:
            None.
        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

        print("An error occurred at request {}: {}".format(request, error))

    @if_connected
    def set_run_status(self):
        """
        Starts the device running to present settings if it is not running.

        Returns:
            ">" : If device's run direction is in infusion mode.
            "<" : If device's run direction is in withdrawing mode.
        """
        if self._device.running_status != RunStatus.Stopped:
            if self._device.running_status == RunStatus.Infusing:
                return self.Infusing
            elif self._device.running_status == RunStatus.Withdrawing:
                return self.Withdrawing
            else:
                print("An error occurred when trying to run the device. The device's running direction \
                    is {} and the running state is {}.".format(
                    self._device.running_direction, self._device.running))

    @if_connected
    def get_run_status(self):
        """
        Gets the run status of the pump.

        Returns:
            ":" : If the device is not running.
            ">" : If device's run direction is in infusion mode.
            "<" : If device's run direction is in withdrawing mode.
        """
        if self._device.running_status == RunStatus.Infusing:
            return self.Infusing
        elif self._device.running_status == RunStatus.Withdrawing:
            return self.Withdrawing
        elif self._device.running_status == RunStatus.Stopped:
            return self.Stopped
        else:
            print("""An error occurred when trying to run the device
                  "The device's running direction is {} and the running state is {}""".format(
                    self._device.running_direction, self._device.running))



