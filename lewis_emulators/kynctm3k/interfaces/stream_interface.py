from lewis.adapters.stream import StreamInterface, Cmd


class Kynctm3KStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("return_data", "MM,1111111111111111$"),
    }

    in_terminator = "\r"
    out_terminator = "\r"

    def return_data(self):
        """
        Returns the data in the format specified in the user manual

        Returns:
            String: A carriage-return separated string of measurments for all OUT values in the program.

        """
        return self._device.format_output_data()

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)
