from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


class NgpspsuStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_version").escape("VER").build(),
        CmdBuilder("turn_on_device").escape("MON").build(),
        CmdBuilder("turn_off_device").escape("MOFF").build()
    }

    out_terminator = "\r"
    in_terminator = "\r\n"

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

    def get_version(self):
        """
        Returns the model number and firmware of the device

        E.g. "#VER:NGPS 100-50:0.9.01" where "NGPS 100-50" is the model
        number and "0.9.01" is the firmware number.
        """
        return "#VER:{}".format(self._device.model_number_and_firmware)

    def turn_on_device(self):
        """
        Turns on the device.

        Returns:
            string: "#AK" if the device is turned on. "#NAK%i" otherwise, where %i is an
                error code.
        """
        return self._device.turn_on_device()

    def turn_off_device(self):
        """
        Turns off the device.

        Returns:
            string: "#AK" if the device is turned on. "#NAK%i" otherwise, where %i is an
                error code.
        """
        return self._device.turn_off_device()
