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
        print("An error occurred at request ", str(request), ": ", str(error))

    def acknowledge_pressure(self, request):
        """
        Acknowledges a request to get the pressure and stores the request.

        Args:
            request: Pressure chanel to read from.

        Returns:
            ASCII acknowledgement character (0x6).
        """

        self._last_command = "P{}".format(request)
        return self.ACK

    def acknowledge_units(self):
        """
        Acknowledge that the request for current units was received.

        Returns:
            ASCII acknowledgement character (0x6).
        """
        self._last_command = "UNI"
        return self.ACK

    def acknowledge_set_units(self, units):
        """
        Acknowledge that the request to set the units was received.

        Args:
            units (integer): unit flag value.

        Returns:
            ASCII acknowledgement character (0x6).
        """

        self._last_command = "UNI{}".format(units)
        return self.ACK

    def handle_enquiry(self):
        """
        Handles an enquiry using the last command sent.

        Returns:
            Channel pressure (string): Returns a string with DEVICE_STATE and
                current channel pressure.
            get_units(): Returns the devices current units.
            set_units(): Sets the devices units.
        """

        if self._last_command in self.channels:
            return self.get_pressure(self._last_command)
        elif self._last_command == "UNI":
            return self.get_units()
        elif self._last_command == "UNI1" or self._last_command == "UNI2" or self._last_command == "UNI3":
            units_value = self._last_command[-1]
            return self.set_units(units_value)
        else:
            print("Last command was unknown: ", str(self._last_command))

    def get_units(self):
        """
        Gets the units of the device.

        Returns:
            units (string): Devices current units: mbar, Torr, or Pa.
        """
        return self._device.units

    def set_units(self, units):
        """
        Sets the units on the device.

        Returns:
            None.
        """

        self._device.units = units

    def get_pressure(self, channel):
        channel_lower_case = channel[-2:].lower()
        pressure_channel = "pressure_{}".format(channel_lower_case)
        pressure = getattr(self._device, pressure_channel)

        return "{},{}".format(self.DEVICE_STATUS, pressure)
