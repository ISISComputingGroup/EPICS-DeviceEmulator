from lewis.adapters.stream import StreamAdapter, Cmd


class InstronStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_control_channel", "^Q300$"),
        Cmd("set_control_channel", "^C300,([1-3])$"),
        Cmd("get_watchdog_status", "^Q904$"),
        Cmd("set_watchdog_status", "^C904,([0-2]),([0-3])$"),
        Cmd("get_control_mode", "^Q909$"),
        Cmd("set_control_mode", "^P909,([0-1])$"),
        Cmd("get_status", "^Q22$"),
        Cmd("arbitrary_command", "^([a-z]*)$"),
        Cmd("get_actuator_status", "^Q23$"),
        Cmd("set_actuator_status", "^C23,([0-1])$"),
        Cmd("get_movement_type", "^Q1$"),
        Cmd("set_movement_type", "^C1,([0-3])$"),
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_control_channel(self):
        return self._device.get_control_channel()

    def set_control_channel(self, channel):
        self._device.set_control_channel(int(channel))

    def get_watchdog_status(self):
        enabled, status = self._device.get_watchdog_status()
        return "{},{}".format(enabled, status)

    def set_watchdog_status(self, cv1, cv2):
        self._device.set_watchdog_status(int(cv1), int(cv2))

    def get_control_mode(self):
        return self._device.get_control_mode()

    def set_control_mode(self, mode):
        self._device.set_control_mode(int(mode))

    def get_status(self):
        return int(self._device.get_status())

    def arbitrary_command(self, command):
        return "Arb_com_response_" + str(command)

    def get_actuator_status(self):
        return self._device.get_actuator_status()

    def set_actuator_status(self, mode):
        self._device.set_actuator_status(int(mode))

    def get_movement_type(self):
        return self._device.get_movement_type()

    def set_movement_type(self, mov_type):
        self._device.set_movement_type(int(mov_type))
