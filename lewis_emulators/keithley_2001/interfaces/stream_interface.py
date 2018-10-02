from lewis.adapters.stream import StreamInterface, has_log
from lewis_emulators.utils.command_builder import CmdBuilder


@has_log
class Keithley2001StreamInterface(StreamInterface):

    in_terminator = "\r\n"
    out_terminator = "\n"

    commands = {
        # Commands used on setup
        CmdBuilder("get_idn").escape("*IDN?").eos().build(),
        CmdBuilder("reset_device").escape("*RST").eos().build(),
        CmdBuilder("set_buffer_source").escape(":DATA:FEED ").arg("NONE|SENS1|CALC1").eos().build(),
        CmdBuilder("get_buffer_source").escape(":DATA:FEED?").eos().build(),
        CmdBuilder("set_buffer_egroup").escape(":DATA:EGR ").arg("FULL|COMP").eos().build(),
        CmdBuilder("get_buffer_egroup").escape(":DATA:EGR?").eos().build(),
        CmdBuilder("set_continuous_scanning_status").escape(":INIT:CONT ").arg("OFF|ON").eos().build(),
        CmdBuilder("get_continuous_scanning_status").escape(":INIT:CONT?").eos().build(),
        CmdBuilder("get_elements").escape(":FORM:ELEM?").eos().build(),
        CmdBuilder("set_elements").escape(":FORM:ELEM ").string().eos().build(),
        CmdBuilder("get_measurement_status").escape(":STAT:MEAS:ENAB?").eos().build(),
        CmdBuilder("set_buffer_full_status").escape(":STAT:MEAS:ENAB 512").eos().build(),
        CmdBuilder("get_service_request_status").escape("*SRE?").eos().build(),
        CmdBuilder("set_measure_summary_status").escape("*SRE 1").eos().build(),
        CmdBuilder("reset_and_clear_status_registers").escape(":STAT:PRES; *CLS").eos().build(),
        CmdBuilder("set_scan_count").escape(":ARM:LAY2:COUN ").int().eos().build(),
        CmdBuilder("get_scan_count").escape(":ARM:LAY2:COUN?").eos().build(),

        # Single channel read
        CmdBuilder("close_channel").escape(":ROUT:CLOS (@").int().escape(")").eos().build(),
        CmdBuilder("read_single_channel").escape(":ABOR;:FETC?").eos().build(),

        # Reading from the buffer
        CmdBuilder("set_buffer_mode").escape(":DATA:FEED:CONT ").arg("NEV|NEXT|ALW|PRET").eos().build(),
        CmdBuilder("get_buffer_mode").escape(":DATA:FEED:CONT?").eos().build(),

        CmdBuilder("set_buffer_size").escape(":DATA:POIN ").int().eos().build(),
        CmdBuilder("get_buffer_size").escape(":DATA:POIN?").eos().build(),
        CmdBuilder("clear_buffer").escape(":DATA:CLE").eos().build()

        # Setting up a scan

    }

    def handle_error(self, request, error):
        self.log.error("An error occurred at request {}: {}".format(repr(request), repr(error)))
        print("An error occurred at request {}: {}".format(repr(request), repr(error)))

    def get_idn(self):
        """
        Returns the devices IDN string.

        Returns:
            string: The device's IDN.
        """

        return self._device.idn

    def get_elements(self):
        """
        Returns the lists of elements of a reading in alphabetical order from the device.

        """
        elements = [element for element, value in self._device.elements.items() if value]
        return ", ".join(elements)

    def set_elements(self, string):
        """
        Sets the elements a reading has.

        Args:
            string: String of comma separated elements of a reading. Valid elements are:
                READ, CHAN, RNUM, UNIT, TIME, STAT.
        """
        elements = {element.strip().upper() for element in string.split(",")}

        for element in elements:
            try:
                self._device.elements[element] = True
            except LookupError:
                self.log.error("Tried to set {} which is not a valid reading element.".format(element))
                print("Tried to set {} which is not a valid reading element.".format(element))

    def reset_device(self):
        """
        Resets device.
        """
        self._device.reset_device()

    def clear_buffer(self):
        """
        Clears the buffer.
        """
        self._device.buffer.clear_buffer()

    def set_buffer_source(self, source):
        """
        Sets the buffer source.
        """
        self._device.buffer.source = source

    def get_buffer_source(self):
        """
        Gets the buffer source.
        """
        return self._device.buffer.source

    def set_buffer_mode(self, mode):
        """
        Sets the buffer mode.
        """
        self._device.buffer.mode = mode

    def get_buffer_mode(self):
        """
        Gets the buffer mode.
        """
        return self._device.buffer.mode

    def set_buffer_size(self, size):
        """
        Sets the buffer mode.
        """
        self._device.buffer.size = int(size)

    def get_buffer_size(self):
        """
        Gets the buffer mode.
        """
        return self._device.buffer.size

    def set_buffer_egroup(self, egroup):
        """
        Sets the buffer element group.
        """
        self._device.buffer.egroup = egroup

    def get_buffer_egroup(self):
        """
        Gets the buffer element group.
        """
        return self._device.buffer.egroup

    def set_continuous_scanning_status(self, value):
        """
        Sets continuous scanning status to ON or OFF.

        Thus is called continuous initialization mode in the Keithley 2001 manual.

        Args:
            value (string): ON or OFF.
        """
        if value.upper() == "ON":
            self._device.continuous_initialisation_status = True
        elif value.upper() == "OFF":
            self._device.continuous_initialisation_status = False
        else:
            raise ValueError("Not a valid continuous initialisation mode")

    def get_continuous_scanning_status(self):
        """
        Gets the continuous scanning status.

        Thus is the continuous initialization mode in the Keithley 2001 manual.
        """
        return_string = "OFF"

        if self._device.continuous_initialisation_status:
            return_string = "ON"

        return return_string

    def close_channel(self, channel):
        """
        Sets the single channel to read from.

        Args:
            channel (int): Channel number to open
        """
        self._device.close_channel(channel)

    def read_single_channel(self):
        channel_data = []
        channel = self._device.channel

        if self._device.elements["READ"]:
            channel_data.append("{:.7E}".format(channel.reading))
        if self._device.elements["UNIT"] and self._device.elements["READ"]:
            channel_data.append("{}".format(channel.unit.name))
        if self._device.elements["CHAN"]:
            channel_data.append(",{}INTCHAN".format(channel.channel))

        return "".join(channel_data)

    def set_buffer_full_status(self):
        self._device.status_register.buffer_full = True

    def set_measure_summary_status(self):
        self._device.status_register.measurement_summary_status = True

    def get_measurement_status(self):
        status = 0
        if self._device.status_register.buffer_full:
            status += 512

        return str(status)

    def get_service_request_status(self):
        status = 0
        if self._device.status_register.measurement_summary_status:
            status += 1

        return str(status)


    def reset_and_clear_status_registers(self):
        """
        Resets and clears the status registers of the device.
        """

        self._device.status_register.reset_and_clear()

    def set_scan_count(self, value):
        """
        Sets the scan count.

        Args:
            value (int): Number of times to scan.
        """
        self._device.scan_count = value

    def get_scan_count(self):
        """
        Returns the number of times the device is set to scan.

        Returns:
            string: Number of times the device is set to scan.
        """
        return str(self._device.scan_count)
