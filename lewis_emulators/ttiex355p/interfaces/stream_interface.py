from lewis.adapters.stream import StreamInterface, Cmd


class TTIEX355PStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("catch_all", "^#9.*$"),  # Catch-all command for debugging
    }

    def catch_all(self):
        pass

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)