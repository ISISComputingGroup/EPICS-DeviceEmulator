from lewis.adapters.stream import StreamAdapter, Cmd
from time import sleep


class CybamanStreamInterface(StreamAdapter):
    """
    Stream interface for the serial port
    """

    commands = {
        Cmd("initialize", "^A$"),
        Cmd("get_a", "^M101$"),
        Cmd("get_b", "^M201$"),
        Cmd("get_c", "^M301$"),
        Cmd("set_all", "^OPEN PROG 10 CLEAR\nG1 A ([0-9]*\.?[0-9]*) B ([0-9]*\.?[0-9]*) C ([0-9]*\.?[0-9]*) TM([0-9]*)$"),
        Cmd("ignore", "^CLOSE$"),
        Cmd("ignore", "^B10R$"),
        Cmd("reset", "^\$\$\$$"),
        Cmd("home_a", "^B9001R$"),
        Cmd("home_b", "^B9002R$"),
        Cmd("home_c", "^B9003R$"),
    }

    in_terminator = "\r"
    out_terminator = chr(0x06) # ACK character

    def handle_error(self, request, error):
        """
        If command is not recognised print and error.

        :param request: requested string
        :param error: problem
        :return:
        """
        print "An error occurred at request " + repr(request) + ": " + repr(error)

    def wait_before_response(self):
        sleep(0.1)

    def ignore(self):
        self.wait_before_response()
        return ""

    def initialize(self):
        self.wait_before_response()
        return ""

    def get_a(self):
        self.wait_before_response()
        print "Returning input A as {}".format(self._device.a)
        return self._device.a*3577

    def get_b(self):
        self.wait_before_response()
        print "Returning input B as {}".format(self._device.b)
        return self._device.b*3663

    def get_c(self):
        self.wait_before_response()
        print "Returning input C as {}".format(self._device.c)
        return self._device.c*3663

    def set_all(self, a, b, c, tm):
        self.wait_before_response()
        self._device.a = float(a)
        self._device.b = float(b)
        self._device.c = float(c)
        return ""

    def reset(self):
        self._device._initialize_data()
        return ""

    def home_a(self):
        self._device.home_axis_a()
        return ""

    def home_b(self):
        self._device.home_axis_b()
        return ""

    def home_c(self):
        self._device.home_axis_c()
        return ""
