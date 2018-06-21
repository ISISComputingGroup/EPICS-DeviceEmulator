from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.if_connected import if_connected

from ..util_classes import RunStatus
from ..util_constants import DIRECTIONS


def if_error(f):
    """
    Decorator that executes f if the device has no errors on it and returns the error prompt otherwise.

    Args:
        f: function to be executed if the device has no error.

    Returns:
       The value of f(*args) if the device has no error and "\r\nE" otherwise.
   """

    def wrapper(*args):
        error = getattr(args[0], "_device").last_error.value
        if error == 0:
            result = f(*args)
        else:
            result = "\r\nE"
        return result
    return wrapper


@has_log
class Sp2XXStreamInterface(StreamInterface):
    """
    Stream interface for the serial port.
    """

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("start").escape("run").eos().build(),
        CmdBuilder("stop").escape("stop").eos().build(),
        CmdBuilder("get_run_status").escape("run?").eos().build(),
        CmdBuilder("get_error_status").escape("error?").eos().build(),
        CmdBuilder("set_mode").escape("mode ").arg("i/w|w/i|i|w|con").eos().build(),
        CmdBuilder("get_mode").escape("mode?").eos().build(),
        CmdBuilder("get_direction").escape("dir?").eos().build(),
        CmdBuilder("reverse_direction").escape("dir rev").eos().build()
    }

    out_terminator = ""
    in_terminator = "\r"

    _return = "\r\n"
    Infusion = "\r\n>"
    Withdrawal = "\r\n<"
    Stopped = "\r\n:"

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

    @if_error
    @if_connected
    def start(self):
        """
        Starts the device running to present settings if it is not running.

        Returns:

        """
        if self._device.running is False:
            if self._device.direction == DIRECTIONS["I"]:
                self._device.start_device()
                return self.Infusion
            elif self._device.direction == DIRECTIONS["W"]:
                self._device.start_device()
                return self.Withdrawal
            else:
                print("An error occurred when trying to run the device. The device's running state is \
                    is {}.".format(
                    self._device.running_direction))

    @if_error
    @if_connected
    def get_run_status(self):
        """
        Gets the run status of the pump.

        Returns:
            "\r\n:" : If the device is not running.
            "\r\n>" : Prompt saying the device's run direction is infusing.
            "\r\n<" : Prompt saying the device's run direction is withdrawing.
        """
        if self._device.running_status == RunStatus.Infusion:
            return self.Infusion
        elif self._device.running_status == RunStatus.Withdrawal:
            return self.Withdrawal
        elif self._device.running_status == RunStatus.Stopped:
            return self.Stopped
        else:
            print("An error occurred when trying to run the device.")

    @if_error
    @if_connected
    def stop(self):
        """
        Stops the device running.
        Returns:
            "\r\n:" : stopped prompt
        """
        self._device.stop_device()
        return self.Stopped

    @if_connected
    def get_error_status(self):
        """
        Gets the error status from the device and returns the error value and run status.

        Returns:
            \r\n%i\r{} where %i is the error_type value and {} the run status.
        """
        last_error = self._device.last_error
        current_status = None

        if self._device.running_status == RunStatus.Infusion:
            current_status = self.Infusion
        elif self._device.running_status == RunStatus.Withdrawal:
            current_status = self.Withdrawal
        elif self._device.running_status == RunStatus.Stopped:
            current_status = self.Stopped

        return "{}{}{}".format(self._return, last_error.value, current_status)

    @if_error
    @if_connected
    def set_mode(self, mode_symbol):
        """
        Sets the mode of the device.

        Args:
            mode_symbol: symbol to change the mode setting

        Returns:
            run_status
        """
        self._device.set_mode(mode_symbol)
        self.stop()

    @if_error
    @if_connected
    def get_mode(self):
        """
        Gets the mode of the device

        Returns:
            The mode the device is in and the run status.
            E.g. \r\nI\r\n: if the device is in infusion mode and stopped.
        """
        mode_response = self._device.mode.response
        run_status = self.get_run_status()
        return "{}{}{}".format(self._return, mode_response, run_status)

    @if_error
    @if_connected
    def get_direction(self):
        """
        Gets the direction of the device

        Returns:
            The direction the device is in and the run status.
            E.g. \r\nI\r: if the device in the infusion direction and stopped.
        """
        run_status = self.get_run_status()
        return "{}{}{}".format(self._return, self._device.direction.symbol, run_status)

    @if_error
    @if_connected
    def reverse_direction(self):
        """
        Reverse the direction of a running device if in infusion or withdrawal mode.

        Returns:
            Run status if the device is running and in infusion or withdrawal mode.
            NA otherwise.
        """
        if self._device.mode.response in ["I", "W"] and self._device.running:
            self._device.reverse_direction()
            self.get_run_status()
        else:
            run_status = self.get_run_status()
            return "{}NA{}".format(self._return, run_status)


