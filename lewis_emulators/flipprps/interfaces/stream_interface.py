from lewis.adapters.stream import StreamInterface, Cmd


class FlipprpsStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("set_polarity_down", "^dn$"),
        Cmd("set_polarity_up", "^up$"),
    }

    terminator = "\r\n"

    def set_polarity_down(self):
        self._device.polarity = 0
        return "OK" + self.terminator

    def set_polarity_up(self):
        self._device.polarity = 1
        return "OK" + self.terminator
