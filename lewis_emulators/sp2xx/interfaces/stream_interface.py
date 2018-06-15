from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.if_connected import if_connected
from ..device import RunStatus, Direction


@has_log
class Sp2XXStreamInterface(StreamInterface):
    """
    Stream interface for the serial port.
    """

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("start").escape("run").eos().build(),
        CmdBuilder("stop").escape("stop").eos().build(),
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
    def start(self):
        """
        Starts the device running to present settings if it is not running.

        Returns:

        """
        if self._device.running is False:
            if self._device.direction == Direction.Infusing:
                self._device.start_device()
                return self.Infusing
            elif self._device.direction == Direction.Withdrawing:
                self._device.start_device()
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
            ">" : Prompt saying the device's run direction is infusing.
            "<" : Prompt saying the device's run direction is withdrawing.
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

    @if_connected
    def stop(self):
        """
        Stops the device running.
        Returns:
            "\r\n:" : stopped prompt
        """
        self._device.stop_device()
        return self.Stopped




