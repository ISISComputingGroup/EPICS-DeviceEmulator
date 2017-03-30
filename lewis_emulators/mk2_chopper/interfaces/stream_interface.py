from lewis.adapters.stream import StreamAdapter, Cmd


class Mk2ChopperStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_true_frequency", "^RF$"),
        Cmd("get_demanded_frequency", "^RG$"),
        Cmd("get_true_phase_delay", "^RP$"),
        Cmd("get_demanded_phase_delay", "^RQ$"),
        Cmd("get_true_phase_error", "^RE$"),
        Cmd("get_demanded_phase_error_window", "^RW$"),
        Cmd("set_chopper_started", "^WS([0-9]+)$"),
        Cmd("set_demanded_frequency", "^WM([0-9]+)$"),
        Cmd("set_demanded_phase_delay", "^WP([0-9]+)$"),
        Cmd("set_demanded_phase_error_window", "^WR([0-9]+)$")
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_demanded_frequency(self):
        return "RG{0:03d}".format(int(self._device.get_demanded_frequency()))

    def get_true_frequency(self):
        return "RF{0:03d}".format(int(self._device.get_true_frequency()))

    def get_demanded_phase_delay(self):
        return "RQ{0:05d}".format(self._device.get_demanded_phase_delay())

    def get_true_phase_delay(self):
        return "RP{0:05d}".format(int(self._device.get_true_phase_delay()))

    def get_demanded_phase_error_window(self):
        return "RW{0:03d}".format(self._device.get_demanded_phase_error_window())

    def get_true_phase_error(self):
        return "RE{0:03d}".format(int(self._device.get_true_phase_error()))

    def set_chopper_started(self, start_flag_raw):
        try:
            start_flag = int(start_flag_raw)
        except ValueError:
            pass
        else:
            if start_flag == 1:
                self._device.start()
            elif start_flag == 2:
                self._device.stop()
        return

    def set_demanded_frequency(self, new_frequency_raw):
        return Mk2ChopperStreamInterface._set(new_frequency_raw, self.get_demanded_frequency,
                                              self._device.set_demanded_frequency)

    def set_demanded_phase_delay(self, new_phase_delay_raw):
        return Mk2ChopperStreamInterface._set(new_phase_delay_raw, self.get_demanded_phase_delay,
                                              self._device.set_demanded_phase_delay)

    def set_demanded_phase_error_window(self, new_phase_error_window_raw):
        return Mk2ChopperStreamInterface._set(new_phase_error_window_raw, self.get_demanded_phase_error_window,
                                              self._device.set_demanded_phase_error_window)

    @staticmethod
    def _set(raw, device_get, device_set):
        try:
            int_value = int(raw)
        except ValueError:
            pass
        else:
            device_set(int_value)
        return device_get()
