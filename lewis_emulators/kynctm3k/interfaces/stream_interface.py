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
        return self._device.format_output_data()

    def change_input_mode(self, new_state):
        return self._device.set_input_mode(new_state)

    def toggle_autosend(self, new_state):
        return self._device.set_autosend_status(int(new_state))

    def handle_error(self, request, error):
        err = "An error occurred at request " + repr(request) + ": " + repr(error)
        print(err)
        self.log.info(err)
        return str(err)
