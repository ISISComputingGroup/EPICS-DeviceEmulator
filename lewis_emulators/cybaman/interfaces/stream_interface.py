from lewis.adapters.stream import StreamAdapter, Cmd


class CybamanStreamInterface(StreamAdapter):
    """
    Stream interface for the serial port
    """

    ACK = chr(0x06) # ACK character

    commands = {
        Cmd("initialize", "^A$"),
    }

    in_terminator = "\r"
    out_terminator = ACK

    def handle_error(self, request, error):
        """
        If command is not recognised print and error.

        :param request: requested string
        :param error: problem
        :return:
        """
        print "An error occurred at request " + repr(request) + ": " + repr(error)

    def initialize(self):
        print "Initializing..."
        return ""
