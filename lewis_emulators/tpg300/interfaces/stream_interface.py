from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


class Tpg300StreamInterface(StreamInterface):
    """
    Stream interface for the serial port.
    """

    _last_command = None
    ACK = chr(6)
    DEVICE_STATUS = 0

    commands = {
        CmdBuilder("acknowledge_pressure").escape("P").arg("A1|A2|B1|B2").build(),
        CmdBuilder("acknowledge_units").escape("UNI").build(),
        CmdBuilder("acknowledge_set_units").escape("UNI").arg("{1|2|3}").build(),
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
        print(self._last_command)

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
            units (integer {1|2|3}): unit flag value.

        Returns:
            ASCII acknowledgement character (0x6).
        """

        self._last_command = "UNI{}".format(units)

        if self._device.connected:
            return self.ACK
        else:
            return

    def _define_channel_lookup(self):
        """
        Defines a lookup dictionary for the 4 pressure channels

        Returns:
            A dictionary which points to the 4 pressure variables
        """

        return {"PA1": self._device.pressure_a1,
                "PA2": self._device.pressure_a2,
                "PB1": self._device.pressure_b1,
                "PB2": self._device.pressure_b2}

    def handle_enquiry(self):
        """
        Handles an enquiry using the last command sent.

        Returns:
            Channel pressure (string): Returns a string with DEVICE_STATE and
                current channel pressure.
            get_units(): Returns the devices current units.
            set_units(): Sets the devices units.
        """

        channel_lookup = self._define_channel_lookup()

        if self._last_command in channel_lookup:
            enquiry_return = "{},{}".format(self.DEVICE_STATUS, channel_lookup[self._last_command])
        elif self._last_command == "UNI":
            enquiry_return = self.get_units()
        elif self._last_command == "UNI{1|2|3}":
            units = self._last_command[-1]
            enquiry_return = self.set_units(units)
        else:
            print("Last command was unknown: ", str(self._last_command))
            enquiry_return = None

        print(self._device.connected)

        if self._device.connected:
            return enquiry_return
        else:
            return None

    def get_units(self):
        """
        Gets the units of the device.

        Returns:
            units (string): Devices current units: mbar, Torr, or Pa.
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

