from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


class MKS_PR4000B_StreamInterface(StreamInterface):
    commands = {
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string
