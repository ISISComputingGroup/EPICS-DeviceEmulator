from lewis.adapters.stream import StreamInterface, Cmd


class IndfurnStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("catch_all", "^#9.*$"),  # Catch-all command for debugging
    }

    def catch_all(self):
        pass
