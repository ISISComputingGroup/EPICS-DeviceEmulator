from lewis.adapters.stream import StreamAdapter, Cmd


class NeoceraStreamInterface(StreamAdapter):

    commands = {
        Cmd("get_state", r"[\r\n]*QISTATE\?[\r\n]*"),
    }

    in_terminator = ";"
    out_terminator = ";"

    def get_state(self):
        return "this is my state"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)

