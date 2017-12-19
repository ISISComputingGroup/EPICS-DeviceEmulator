from lewis.adapters.stream import StreamInterface, Cmd
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.triton.device import SUBSYSTEM_NAMES


class TritonStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_mc_uid").escape("READ:SYS:DR:CHAN:MC").build(),

        # PID setpoints
        CmdBuilder("set_p").escape("SET:DEV:{}:TEMP:LOOP:P:".format(SUBSYSTEM_NAMES["mixing chamber"])).float().build(),
        CmdBuilder("set_i").escape("SET:DEV:{}:TEMP:LOOP:I:".format(SUBSYSTEM_NAMES["mixing chamber"])).float().build(),
        CmdBuilder("set_d").escape("SET:DEV:{}:TEMP:LOOP:D:".format(SUBSYSTEM_NAMES["mixing chamber"])).float().build(),

        # PID readbacks
        CmdBuilder("get_p").escape("READ:DEV:{}:TEMP:LOOP:P".format(SUBSYSTEM_NAMES["mixing chamber"])).build(),
        CmdBuilder("get_i").escape("READ:DEV:{}:TEMP:LOOP:I".format(SUBSYSTEM_NAMES["mixing chamber"])).build(),
        CmdBuilder("get_d").escape("READ:DEV:{}:TEMP:LOOP:D".format(SUBSYSTEM_NAMES["mixing chamber"])).build(),
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def get_mc_uid(self):
        return "STAT:SYS:DR:CHAN:MC:{}".format(SUBSYSTEM_NAMES["mixing chamber"])

    def set_p(self, value):
        self.device.set_p(value)
        return "ok"

    def set_i(self, value):
        self.device.set_i(value)
        return "ok"

    def set_d(self, value):
        self.device.set_d(value)
        return "ok"

    def get_p(self):
        return "STAT:DEV:{}:TEMP:LOOP:P:{}".format(SUBSYSTEM_NAMES["mixing chamber"], self.device.get_p())

    def get_i(self):
        return "STAT:DEV:{}:TEMP:LOOP:I:{}".format(SUBSYSTEM_NAMES["mixing chamber"], self.device.get_i())

    def get_d(self):
        return "STAT:DEV:{}:TEMP:LOOP:D:{}".format(SUBSYSTEM_NAMES["mixing chamber"], self.device.get_d())
