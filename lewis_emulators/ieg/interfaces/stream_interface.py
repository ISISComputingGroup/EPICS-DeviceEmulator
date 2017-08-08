from lewis.adapters.stream import StreamAdapter, Cmd


class IegStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        # Cmd("get_all_data", "^#00000([0-9A-F]{2})\$$"),
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)
