from lewis.adapters.stream import StreamAdapter, Cmd


class FermichopperStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_zero", "^i_want_zero$"),
    }

    in_terminator = ""
    out_terminator = ""

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_zero(self):
        return 0
