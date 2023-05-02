from lewis.adapters.stream import StreamInterface
from lewis.utils.command_builder import CmdBuilder
from ..device import ReadState, Units, FunctionsSet, FunctionsRead, CircuitAssignment
from lewis.utils.replies import conditional_reply
from lewis.utils.constants import ACK
from lewis.core.logging import has_log


@has_log
class Tpgx00StreamInterfaceBase(object):
    """
    Stream interface for the serial port for either a TPG300 or TPG500.
    """

    DEVICE_STATUS = 0

    commands = {
        CmdBuilder("acknowledge_pressure").escape("P").arg("A1|A2|B1|B2").eos().build(),
        CmdBuilder("acknowledge_units").escape("UNI").eos().build(),
        CmdBuilder("acknowledge_set_units").escape("UNI").escape(",").arg("1|2|3").eos().build(),
        CmdBuilder("acknowledge_function").escape("SP").arg("1|2|3|4|A|B").eos().build(),
        CmdBuilder("acknowledge_set_function").escape("SP").arg("1|2|3|4|A|B").escape(",")
        .arg(r"[+-]?\d+.\d+", float).escape("E").arg(r"(?:-|\+)(?:[1-9]+\d*|0)", int).escape(",")
        .arg(r"[+-]?\d+.\d+", float).escape("E").arg(r"(?:-|\+)(?:[1-9]+\d*|0)", int).escape(",").int().eos().build(),
        CmdBuilder("acknowledge_function_status").escape("SPS").eos().build(),
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
        self._device.readstate = ReadState["UNI" + str(units)]
        return ACK

    @conditional_reply("connected")
    def acknowledge_function(self, function):
        """
        Acknowledge that the request for function thresholds was received.

        Args:
            function (string): Takes the value 1, 2, 3, 4, A or B. This it the switching
            function's settings that we want to read.

        Returns:
            ASCII acknowledgement character (0x6).
        """

        self._device.readstate = ReadState["F" + function]
        return ACK

    @conditional_reply("connected")
    def acknowledge_set_function(self, function, low_thr, low_exp, high_thr, high_exp, assign):
        """
        Acknowledge that the request to set the function thresholds was received.

        Args:
            function (string): Takes the value 1, 2, 3, 4, A or B. This it the switching
            function's settings that we want to set.

            low_thr (float): Lower threshold of the switching function.

            low_exp (int): Exponent of the lower threshold.

            high_thr (float): Upper threshold of the switching function.

            high_exp (int): Exponent of the upper threshold.

            assign: Circuit to be assigned to this switching function.

        Returns:
            ASCII acknowledgement character (0x6).
        """
        self._device.readstate = ReadState["FS" + function]
        self._device.switching_function_to_set = CircuitAssignment(low_thr, low_exp, high_thr, high_exp, assign)
        return ACK

    @conditional_reply("connected")
    def acknowledge_function_status(self):
        """
        Acknowledge that the request to check switching functions status was received

        Returns:
            ASCII acknowledgement character (0x6).
        """
        self._device.readstate = ReadState["SPS"]
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
        switching_functions_read = ("F1", "F2", "F3", "F4", "FA", "FB")
        switching_functions_set = ("FS1", "FS2", "FS3", "FS4", "FSA", "FSB")
        units_flags = ("UNI1", "UNI2", "UNI3")

        if self._device.readstate.name in channels:
            return self.get_pressure(self._device.readstate)

        elif self._device.readstate.name == "UNI":
            return self.get_units()

        elif self._device.readstate.name in units_flags:
            return self.set_units(Units(self._device.readstate.value))

        elif self._device.readstate.name in switching_functions_read:
            return self.get_thresholds_readstate(self._device.readstate.value)

        elif self._device.readstate.name in switching_functions_set:
            self.set_threshold(self._device.readstate.value)
            readstate = str(self._device.readstate.value).replace("S", "", 1)
            return self.get_thresholds_readstate(readstate)

        elif self._device.readstate.name == "SPS":
            status = self.get_switching_functions_status()
            return str(status[0]) + ',' + str(status[1]) + ',' + str(status[2]) + \
                   ',' + str(status[3]) + ',' + str(status[4]) + ',' + str(status[5])

        else:
            self.log.info("Last command was unknown. Current readstate is {}.".format(self._device.readstate))

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
        return units.value

    def get_threshold(self, function):
        """
        Sets the settings of a switching function.

        Returns:
            tuple containing a sequence of: high_threshold (float), high_exponent(int),
            low_threshold (float), low_exponent (int), circuit_assignment (1|2|2|4|A|B)
        """
        index = FunctionsRead[function].value
        return self._device.switching_functions[index]

    def set_threshold(self, function):
        """
        Sets the settings of a switching function.

        Args:
            function: tuple containing a sequence of: high_threshold (float), high_exponent(int),
            low_threshold (float), low_exponent (int), circuit_assignment (1|2|2|4|A|B)

        Returns:
            None.
        """
        index = FunctionsSet[function].value
        self._device.switching_functions[index] = self._device.switching_function_to_set

    def get_thresholds_readstate(self, readstate):
        """
        Helper method for getting thresholds of a function all in one string based on current readstate.

        Returns:
            a string containing thresholds information
        """
        function = self.get_threshold(readstate)
        return str(function.high_threshold) + "E" + str(function.high_exponent) + "," + \
               str(function.low_threshold) + "E" + str(function.low_exponent) + "," + str(function.circuit_assignment)

    def get_switching_functions_status(self):
        """
        Returns statuses of switching functions

        Returns:
            a list of 6 zeros or ones (on/off) for each function
        """
        return self._device.switching_functions_status

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

   
class Tpg300StreamInterface(Tpgx00StreamInterfaceBase, StreamInterface):
    protocol = 'tpg300'


class Tpg500StreamInterface(Tpgx00StreamInterfaceBase, StreamInterface):
    protocol = 'tpg500'
