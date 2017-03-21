from lewis.adapters.stream import StreamAdapter, Cmd


class HRPDSampleChangerStreamInterface(StreamAdapter):

    commands = {
        Cmd("get_id", "^id$"),
        Cmd("get_position", "^po$"),
        Cmd("get_status", "^st$"),
        Cmd("go_back", "^bk$"),
        Cmd("go_fwd", "^fw$"),
        Cmd("halt", "^ht$"),
        Cmd("initialise", "^in$"),
        Cmd("lower_arm", "^lo$"),
        Cmd("move_to", "^ma([0-9]{2})$", argument_mappings=[int]),
        Cmd("move_to_without_lowering", "^mn([0-9]{2})$", argument_mappings=[int]),
        Cmd("raise_arm", "^ra$"),
        Cmd("read_variable", "^vr([0-9]{4})$", argument_mappings=[int])
    }

    in_terminator = "\r"
    out_terminator = "\r\n"

    def _check_error_code(self, code):
        if code == self._device.NO_ERR:
            return "ok"
        else:
            return "rf-%02d" % code

    def get_id(self):
        return "0001 0001 ISIS HRPD Sample Changer V1.00"

    def get_position(self):
        return "Position = " + str(self._device.carousel_position)

    def get_status(self):
        return str(self._device.get_status())

    def go_back(self):
        return self._check_error_code(self._device.go_backward())

    def go_fwd(self):
        return self._check_error_code(self._device.go_forward())

    def read_variable(self, variable):
        return "READ VARIABLE  " + str(variable)

    def halt(self):
        return "ok"

    def initialise(self):
        return self._check_error_code(self._device.init())

    def move_to(self, position):
        return self._check_error_code(self._device.move_to(position, True))

    def move_to_without_lowering(self, position):
        return self._check_error_code(self._device.move_to(position, False))

    def lower_arm(self):
        return self._check_error_code(self._device.set_arm(True))

    def raise_arm(self):
        return self._check_error_code(self._device.set_arm(False))

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)

