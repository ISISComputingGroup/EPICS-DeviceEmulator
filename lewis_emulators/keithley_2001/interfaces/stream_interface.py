from lewis.adapters.stream import StreamInterface, has_log
from lewis_emulators.utils.command_builder import CmdBuilder


@has_log
class Keithley2001StreamInterface(StreamInterface):

    in_terminator = "\n"
    out_terminator = in_terminator

    commands = {
        CmdBuilder("get_idn").escape("*IDN?").build(),
        CmdBuilder("reset").escape("*RST").build(),
        CmdBuilder("get_elements").escape(":FORM:ELEM?").build(),
        CmdBuilder("set_elements").escape(":FORM:ELEM ").string().build()
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
            string: String of comma separated elements of a reading. Valid elemetns are:
                READ, CHAN, RNUM, UNIT, TIME, STAT.
        """
        elements = {element.strip().upper() for element in string.split(",")}

        for element in elements:
            try:
                self._device.elements[element] = True
            except LookupError:
                self.log.error("Tried to set {} which is not a valid reading element.".format(element))
                print("Tried to set {} which is not a valid reading element.".format(element))

    def reset(self):
        """
        Resets device.
        """
        self._device.reset_device()
