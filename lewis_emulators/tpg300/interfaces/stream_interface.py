from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder
from ..device import ReadState, Units
from lewis_emulators.utils.replies import conditional_reply
from lewis_emulators.utils.constants import ACK


class Tpg300StreamInterface(StreamInterface):
    """
    Stream interface for the serial port.
    """

    DEVICE_STATUS = 0

    commands = {
        CmdBuilder("acknowledge_pressure").escape("P").arg("A1|A2|B1|B2").eos().build(),
        CmdBuilder("acknowledge_units").escape("UNI").eos().build(),
        CmdBuilder("acknowledge_set_units").escape("UNI").arg("1|2|3").eos().build(),
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

    @conditional_reply("connected")
    def acknowledge_pressure(self, channel):
        """
        Acknowledges a request to get the pressure and stores the request.

        Args:
            channel: Pressure chanel to read from.

        Returns:
            ASCII acknowledgement character (0x6).
        """

        self._device.readstate = ReadState[channel]
        return ACK

    @conditional_reply("connected")
    def acknowledge_units(self):
        """
        Acknowledge that the request for current units was received.

        Returns:
            ASCII acknowledgement character (0x6).
        """

        self._device.readstate = ReadState["UNI"]
        return ACK

    @conditional_reply("connected")
    def acknowledge_set_units(self, units):
        """
        Acknowledge that the request to set the units was received.

        Args:
            units (integer): Takes the value 1, 2 or 3.

        Returns:
            ASCII acknowledgement character (0x6).
        """
        self._device.readstate = ReadState(units)
        return ACK

    def handle_enquiry(self):
        """
        Handles an enquiry using the last command sent.

        Returns:
            String: Channel pressure if last command was in channels.
            String: Returns the devices current units if last command is 'UNI'.
            None: Sets the devices units to 1,2, or 3 if last command is 'UNI{}' where {} is 1, 2 or 3
                respectively.
            None: Last command unknown.
        """
        self.log.info(self._device.readstate)

        channels = ("A1", "A2", "B1", "B2")
        units_flags = range(1, 4)

        if self._device.readstate.name in channels:
            return self.get_pressure(self._device.readstate)

        elif self._device.readstate.name == "UNI":
            return self.get_units()

        elif self._device.readstate.value in units_flags:
            return self.set_units(Units(self._device.readstate.value))

        else:
            print("Last command was unknown. Current readstate is {}.". format(self._device.readstate))

    def get_units(self):
        """
        Gets the units of the device.

        Returns:
            Name of the units.
        """
        return self._device.units.value

    def set_units(self, units):
        """
        Sets the units on the device.

        Args:
            units (Units member): Units to be set

        Returns:
            None.
        """
        self._device.units = units

    def get_pressure(self, channel):
        """
        Gets the pressure for a channel.

        Args:
            channel (Enum member): Enum readstate pressure channel. E.g. Readstate.A1.

        Returns:
            String: Device status and pressure from the channel.
        """

        pressure_channel = "pressure_{}".format(channel.value)
        pressure = getattr(self._device, pressure_channel)

        return "{},{}".format(self.DEVICE_STATUS, pressure)
