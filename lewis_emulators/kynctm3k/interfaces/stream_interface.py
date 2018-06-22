from lewis.adapters.stream import StreamInterface, Cmd


class Kynctm3KStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("catch_all", "^.*$"),  # Catch-all command for debugging
    }

    in_terminator = "\r"
    out_terminator = "\r"

    def catch_all(self):
        return "Hello, world!"
