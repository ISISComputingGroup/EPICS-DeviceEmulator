from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log


@has_log
class Kynctm3KStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("return_data", "MM,1111111111111111$"),
        Cmd("change_input_mode", "(Q0|R0|R1)$"),
        Cmd("toggle_autosend", "SW,EA,(1|0)$")
    }

    in_terminator = "\r"
    out_terminator = "\r"

    def return_data(self):
        """
        Returns the data in the format specified in the user manual

        Returns:
            String: A carriage-return separated string of measurments for all OUT values in the program.

        """
        self.log.info("Actual output string: "+self._device.format_output_data())
        return self._device.format_output_data()

    def change_input_mode(self, new_state):
        self.log.info("New state: {}".format(new_state))
        return self._device.set_input_mode(new_state)

    def toggle_autosend(self, new_state):
        a = self._device.set_autosend_status(new_state)
        self.log.info(a)
        return a#self._device.set_autosend_status(new_state)

    def handle_error(self, request, error):
        err = "An error occurred at request " + repr(request) + ": " + repr(error)
        print(err)
        self.log.info(err)
        return str(err)
