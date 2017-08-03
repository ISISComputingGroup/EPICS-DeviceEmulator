from lewis.adapters.stream import StreamAdapter
from lewis_emulators.utils.command_builder import CmdBuilder


class SuperlogicsStreamInterface(StreamAdapter):
    """
    Stream interface for the serial port
    """

    commands = {
        CmdBuilder("get_values").escape("#").arg("[0-9]+").build(),
        CmdBuilder("get_version").escape("$").arg("[0-9]+").escape("F").build()
    }

    in_terminator = "\r"
    out_terminator = "\r"

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        print "An error occurred at request " + repr(request) + ": " + repr(error)

    def get_values(self, address):
        """
        Gets the values from the device

        Returns: List of values, one for each connected channel
        """
        if self._device.disconnected:
            return None

        values = self._device.values_1 if address == "01" else self._device.values_2
        formatted_values = map(lambda s: "+{0:.2f}".format(s), values)
        return ",".join(formatted_values)

    def get_version(self, address):
        """
        Get the firmware version from the device
        :param address: the address to read the version from
        :return: string representing the firmware version for the address
        """
        if self._device.disconnected:
            return None

        version = self._device.version_1 if address == "01" else self._device.version_2
        return "!{0}{1}".format(address, version)
