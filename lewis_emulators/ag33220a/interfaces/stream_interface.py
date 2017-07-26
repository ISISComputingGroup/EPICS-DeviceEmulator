from lewis.adapters.stream import StreamAdapter, Cmd

class AG33220AStreamInterface(StreamAdapter):

    commands = {
        Cmd("get_voltage", "^VOLT\?$"),
        Cmd("set_voltage", "^VOLT " + "([\-0-9.]+)$", argument_mappings=[float]),
        Cmd("get_freq", "^FREQ\?$"),
        Cmd("set_freq", "^FREQ " + "([\-0-9.]+)$", argument_mappings=[float]),
        Cmd("get_offset", "^VOLT:OFFS\?$"),
        Cmd("set_offset", "^VOLT:OFFS " + "([\-0-9.]+)$", argument_mappings=[float]),
        Cmd("get_units", "^VOLT:UNIT\?$"),
        Cmd("set_units", "^VOLT:UNIT " + "(VPP|VRMS|DBM)$", argument_mappings=[str]),
        Cmd("get_function", "^FUNC\?$"),
        Cmd("set_function", "^FUNC " + "(SIN|SQU|RAMP|PULS|NOIS|DC|USER)$", argument_mappings=[str]),
        Cmd("get_output", "^OUTP\?$"),
        Cmd("set_output", "^OUTP " + "(0|1|ON|OFF)$", argument_mappings=[str]),
        Cmd("get_idn", "^\*IDN\?$"),

    }

    in_terminator = "\n"
    out_terminator = "\n"

    def get_voltage(self):
        return self._device.voltage

    def set_voltage(self, new_voltage):
        self._device.voltage = new_voltage

    def get_freq(self):
        return self._device.frequency

    def set_freq(self, new_frequency):
        self._device.frequency = new_frequency

    def get_offset(self):
        return self._device.offset

    def set_offset(self, new_offset):
        self._device.offset = new_offset

    def get_units(self):
        return self._device.units

    def set_units(self, new_units):
        self._device.units = new_units

    def get_function(self):
        return self._device.function

    def set_function(self, new_function):
        self._device.function = new_function

    def get_output(self):
        return self._device.output

    def set_output(self, new_output):
        try:
            new_output = int(new_output)
        except:
            new_output = ["OFF", "ON"].index(new_output)
        self._device.output = new_output

    def get_idn(self):
        return self._device.idn


###################
#    def get_reading(self):
#        rand = random.random() * 100.0
#        min_width = 10
#        data_str = "READ:" + "{:0.3f}".format(rand).ljust(min_width) + ";" + str(self._device.setpoint_mode)
#        return self.create_response(READING_COMM + "  ", data=data_str)
#
#    def handle_error(self, request, error):
#        print "An error occurred at request " + repr(request) + ": " + repr(error)
####################
