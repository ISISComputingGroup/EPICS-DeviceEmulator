from lewis.adapters.stream import StreamAdapter, Cmd


class Mk2ChopperStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_demanded_frequency", "^RG$"),
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_demanded_frequency(self):
        return self._device.get_demanded_frequency()