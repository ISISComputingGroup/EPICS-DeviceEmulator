from lewis.adapters.stream import StreamAdapter, Cmd


class FermichopperStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_data", "^.*$"),
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_data(self):
        # This is "known good" example data from the documentation.
        return "#10003F4"

