from __future__ import print_function, absolute_import, division
from lewis.adapters.stream import StreamInterface
from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply

if_connected = conditional_reply("connected")

EXPECTED_ADDRESSES = ["01", "02"]


class SuperlogicsStreamInterface(StreamInterface):
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
        print("An error occurred at request {}: {}".format(request, error))

    @if_connected
    def get_values(self, address):
        """
        Gets the values from the device

        Returns: List of values, one for each connected channel
        """
        if address not in EXPECTED_ADDRESSES:
            raise ValueError("Invalid address '{}'".format(address))

        values = self._device.values_1 if address == "01" else self._device.values_2
        formatted_values = map(lambda s: "+{0:.2f}".format(s), values)
        return ",".join(formatted_values)

    @if_connected
    def get_version(self, address):
        """
        Get the firmware version from the device
        :param address: the address to read the version from
        :return: string representing the firmware version for the address
        """
        if address not in EXPECTED_ADDRESSES:
            raise ValueError("Invalid address '{}'".format(address))

        version = self._device.version_1 if address == "01" else self._device.version_2
        return "!{0}{1}".format(address, version)
