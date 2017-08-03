from lewis.adapters.stream import StreamAdapter, Cmd
from lewis.core.logging import has_log


@has_log
class RknpsStreamInterface(StreamAdapter):
    """
    Stream interface for the serial port
    """

    in_terminator = "\r"
    out_terminator = "\n\r"

    commands = {
        Cmd("set_adr", "^ADR (001|002)$"),
        Cmd("get_adr", "^ADR$"),
        Cmd("get_ra", "^RA$"),
        Cmd("get_adc", "^AD (\d)"),
        Cmd("get_cmd", "^CMD$"),
        Cmd("set_cmd", "^(LOC|REM)$"),
        Cmd("get_pol", "^PO$"),
        Cmd("set_pol", "^(\+|-)$"),
        Cmd("get_status", "^S1$"),
        Cmd("set_power", "^(F|N)$"),
        Cmd("set_da", "^DA (\d) (-?\d+)$"),
        Cmd("reset", "^RS$")
    }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error.

        Args:
            request: requested string.
            error: problem.
        """
        print "An error occurred at request " + repr(request) + ": " + repr(error)

    def set_adr(self, address):
        """
        Sets the active address.

        Args:
            address: The address to use for the following commands.
        """
        self._device._active_adr = address

    def get_adr(self):
        """
        Gets the active address.

        Returns: a string address.
        """
        return "{0}".format(self._device.adr)

    def get_ra(self):
        """
        Gets the value for RA.

        Returns: a number in 10e-4 Amps.
        """
        return "{0}".format(self._device.ra)

    def get_adc(self, channel):
        """
        Get the value for the specified AD.

        Uses the default channels of 0 for current and 8 for voltage.

        Args:
            channel: The AD to return.

        Returns: a number in either 10e-4 Amps, or in Volts.
        """
        if channel == "2":
            # Channel 2 is the AD for the voltage
            return "{0}".format(self._device.ad_volt)
        elif channel == "8":
            # Channel 0 is the AD for the current
            return "{0}".format(self._device.ad_curr)
        # All other channels are not considered under the requirements of this emulator

    def get_cmd(self):
        """
        Check whether the device is in Local/Remote mode.

        Returns: LOC for local mode, REM for remote mode.
        """
        return "{0}".format(self._device.cmd)

    def set_cmd(self, cmd):
        """
        Sets the active address to be in local or remote mode.

        Args:
            cmd: The mode to set.
        """
        self._device._cmd[self._device._active_adr] = cmd

    def get_pol(self):
        """
        Get the polarity of the device.

        Returns: The polarity as +/-.
        """
        return "{0}".format(self._device.pol)

    def set_pol(self, pol):
        """
        Set the polarity of the device.

        Args:
            pol: The polarity to set.
        """
        self._device._pol[self._device._active_adr] = pol

    def get_status(self):
        """
        Get the status of the device.

        Returns: A character string for the status.
        """
        return "{0}".format(self._device.status)

    def set_power(self, power):
        """
        Turn the output power of the PSU on or off.

        Args:
            power: Whether to turn the PSU oN or ofF.
        """
        self._device.set_power(power)

    def set_da(self, channel, value):
        """
        Set a value for the appropriate DA.

        Considers only the channel for current.

        Args:
            channel: The DA to apply the value to.
            value: The value to apply.
        """
        if channel == "0":
            # Channel 0 is the DA for the current
            self._device.set_current(int(value))
        # All other channels are not considered under the requirements of this emulator

    def reset(self):
        """
        Reset the device, turn it off and set all values to 0.
        """
        self._device.reset()

