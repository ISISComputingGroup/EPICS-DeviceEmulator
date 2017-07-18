from lewis.adapters.stream import StreamAdapter, Cmd


class FermichopperStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_data", "^#0000000\$$"),
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_data(self):
        # This is "known good" example data from the documentation.
        return "#10003F4#2003F0B#3177002#4177003#55F9019#60001F7#75F8B2C#80001F9#90012FC#A00C81C#B020004#C012C19#D012C1A#E012C1B$"
