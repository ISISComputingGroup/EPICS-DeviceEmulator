from lewis.adapters.stream import StreamInterface, has_log
from lewis_emulators.utils.command_builder import CmdBuilder

@has_log
class Keithley2001StreamInterface(StreamInterface):

    in_terminator = "\n"
    out_terminator = in_terminator

    commands = {
        CmdBuilder("get_idn").escape("*IDN?").eos().build(),
        CmdBuilder("reset_device").escape("*RST").eos().build(),
        CmdBuilder("clear_buffer").escape(":DATA:CLE").eos().build(),

        CmdBuilder("set_buffer_source").escape(":DATA:FEED ").arg("NONE|SENS1|CALC1").eos().build(),
        CmdBuilder("get_buffer_source").escape(":DATA:FEED?").eos().build(),

        CmdBuilder("set_buffer_mode").escape(":DATA:FEED:CONT ").arg("NEV|NEXT|ALW|PRET").eos().build(),
        CmdBuilder("get_buffer_mode").escape(":DATA:FEED:CONT?").eos().build(),

        CmdBuilder("set_buffer_egroup").escape(":DATA:EGR ").arg("FULL|COMP").eos().build(),
        CmdBuilder("get_buffer_egroup").escape(":DATA:EGR?").eos().build(),

        CmdBuilder("set_continuous_scanning_status").escape(":INIT:CONT ").arg("OFF|ON").eos().build(),
        CmdBuilder("get_continuous_scanning_status").escape(":INIT:CONT?").eos().build(),

        CmdBuilder("set_buffer_size").escape(":DATA:POIN ").int().eos().build(),
        CmdBuilder("get_buffer_size").escape(":DATA:POIN?").eos().build(),

        CmdBuilder("get_elements").escape(":FORM:ELEM?").eos().build(),
        CmdBuilder("set_elements").escape(":FORM:ELEM ").string().eos().build(),

        CmdBuilder("close_channel").escape(":ROUT:CLOS (@").int().escape(")").eos().build(),
        CmdBuilder("read_single_channel").escape(":FETC?").eos().build()
    }

    def handle_error(self, request, error):
        self.log.error("An error occurred at request {}: {}".format(repr(request), repr(error)))
        print("An error occurred at request {}: {}".format(repr(request), repr(error)))

    def get_idn(self):
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
        self._device.continuous_scanning_status = value

    def get_continuous_scanning_status(self):
        """
        Gets the continuous scanning status.

        Thus is the continuous initialization mode in the Keithley 2001 manual.
        """
        return self._device.continuous_scanning_status

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
