from lewis.adapters.stream import StreamInterface, Cmd


class Kynctm3KStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("return_data", "MA$"),
    }

    in_terminator = "\r"
    out_terminator = "\r"

    def return_data(self):
        return self._device.format_output_data()

    def catch_all(self):
        return "Hello, world!"

    def catch_other(self):
        return "Hello, world!"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)
