from lewis.adapters.stream import StreamInterface, Cmd


class SkfMb350ChopperStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_number", "^get_number$"),
    }

    in_terminator = "\r"
    out_terminator = "\r"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_number(self):
        return 2.0
