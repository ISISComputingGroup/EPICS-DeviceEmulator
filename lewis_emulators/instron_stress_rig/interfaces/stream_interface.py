from lewis.adapters.stream import StreamAdapter, Cmd


class InstronStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_control_channel", "^Q300$"),
        Cmd("set_control_channel", "^C300,([1-3])$"),
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_control_channel(self):
        return self._device.get_control_channel()

    def set_control_channel(self, channel):
        self._device.set_control_channel(channel)
