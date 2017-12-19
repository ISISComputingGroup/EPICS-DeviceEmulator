from lewis.adapters.stream import StreamInterface, Cmd


class TritonStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_mc_uid", "^READ:SYS:DR:CHAN:MC$"),  # Catch-all command for debugging
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def get_mc_uid(self):
        return "STAT:SYS:DR:CHAN:MC:{}".format("mix_chamber_name")
