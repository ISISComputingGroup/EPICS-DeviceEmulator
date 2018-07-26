from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


class NgpspsuStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_version").escape("VER").build(),
        CmdBuilder("start").escape("MON").build(),
        CmdBuilder("stop").escape("MOFF").build(),
        CmdBuilder("read_status").escape("MST").build(),
        CmdBuilder("reset").escape("MRESET").build(),
        CmdBuilder("get_voltage").escape("MRV").build()
    }

    out_terminator = "\r\n"
    in_terminator = "\r"

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

    def start(self):
        """
        Turns on the device.

        Returns:
            string: "#AK" if the device is turned on. "#NAK%i" otherwise, where %i is an
                error code.
        """
        return self._device.start_device()

    def stop(self):
        """
        Turns off the device.

        Returns:
            string: "#AK" if the device is turned on. "#NAK%i" otherwise, where %i is an
                error code.
        """
        return self._device.stop_device()

    def read_status(self):
        """
        Gets the status of the device

        Returns:
            The status of the device which is composed of 8 hexadecimal digts.
        """
        return "#MST:{}".format(self._device.status)

    def reset(self):
        """
        Resets the device.

        Returns:
            string: "#AK" if the device is turned on. "#NAK%i" otherwise, where %i is an
                error code.
        """
        return self._device.reset_device()

    def get_voltage(self):
        """
        Gets the status of the device

        Returns:
            The status of the device which is composed of 8 hexadecimal digts.
        """
        return "#MRV:{}".format(self._device.voltage)

