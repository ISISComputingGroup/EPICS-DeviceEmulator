from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


class Tpg300StreamInterface(StreamInterface):
    """
    Stream interface for the serial port.
    """

    _last_command = None
    ACK = chr(6)
    DEVICE_STATUS = 0
    channels = ("PA1", "PA2", "PB1", "PB2")

    commands = {
        CmdBuilder("acknowledge_pressure").escape("P").arg("A1|A2|B1|B2").build(),
        CmdBuilder("acknowledge_units").escape("UNI").build(),
        CmdBuilder("acknowledge_set_units").escape("UNI").arg("1|2|3").build(),
        CmdBuilder("handle_enquiry").enq().build()
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    @staticmethod
    def handle_error(request, error):
        """
        Prints an error message if a command is not recognised.

        Args:
            request : Request.
            error: The error that has occurred.
        Returns:
            None.
        """
        print("An error occurred at request {}: {}".format(request, error))

    def acknowledge_pressure(self, request):
        """
        Acknowledges a request to get the pressure and stores the request.

        Args:
            request: Pressure chanel to read from.

        Returns:
            ASCII acknowledgement character (0x6).
        """

        self._last_command = "P{}".format(request)

        if self._device.connected:
            return self.ACK
        else:
            return None

    def acknowledge_units(self):
        """
        Acknowledge that the request for current units was received.

        Returns:
            ASCII acknowledgement character (0x6).
        """
        self._last_command = "UNI"

        if self._device.connected:
            return self.ACK
        else:
            return None

    def acknowledge_set_units(self, units):
        """
        Acknowledge that the request to set the units was received.

        Args:
            units (integer): unit flag value. Takes the value 1, 2 or 3.

        Returns:
            ASCII acknowledgement character (0x6).
        """

        self._last_command = "UNI{}".format(units)

        if self._device.connected:
            return self.ACK
        else:
            return

    def handle_enquiry(self):
        """
        Handles an enquiry using the last command sent.

        Returns:
            String: Channel pressure if last command was in channels.
            String: Returns the devices current units if last command is 'UNI'.
            None: Sets the devices units to 1,2, or 3 if last command is 'UNI{}' where {} is 1, 2 or 3
                respectively.
        """

        channel_lookup = self._define_channel_lookup()

        change_unit_commands = ("UNI1", "UNI2", "UNI3")

        if self._last_command in channel_lookup:
            enquiry_return = self.get_pressure(self._last_command)

        elif self._last_command == "UNI":
            enquiry_return = self.get_units()

        elif self._last_command in change_unit_commands:
            units_value = self._last_command[-1]
            enquiry_return = self.set_units(units_value)

        else:
            print("Last command was unknown: ", str(self._last_command))
            enquiry_return = None

        if self._device.connected:
            return enquiry_return
        else:
            return None

    def get_units(self):
        """
        Gets the units of the device.

        Returns:
            String: Devices current units from (mbar, Torr, or Pa).
        """

        if self._device.connected:
            return self._device.units
        else:
            return None

    def set_units(self, units):
        """
        Sets the units on the device.

        Returns:
            None.
        """

        if self._device.connected:
            self._device.units = units

    def get_pressure(self, channel):
        """
        Gets the pressure for a channel.

        Args:
            channel (string): channel name. E.g. PA1.

        Returns:
            String: Device status and pressure from the channel.
        """
        channel_lower_case = channel[-2:].lower()
        pressure_channel = "pressure_{}".format(channel_lower_case)
        pressure = getattr(self._device, pressure_channel)

        return "{},{}".format(self.DEVICE_STATUS, pressure)
