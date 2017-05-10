from lewis.adapters.stream import StreamAdapter, Cmd


class InstronStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_control_channel", "^Q300$"),
        Cmd("set_control_channel", "^C300,([1-3])$"),
        Cmd("get_watchdog_status", "^Q904$"),
        Cmd("set_watchdog_status", "^C904,([0-2]),([0-3])$"),
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

    def get_watchdog_status(self):
        enabled, status = self._device.get_watchdog_status()
        return "{},{}".format(enabled, status)

    def set_watchdog_status(self, cv1, cv2):
        self._device.set_watchdog_status(cv1, cv2)
