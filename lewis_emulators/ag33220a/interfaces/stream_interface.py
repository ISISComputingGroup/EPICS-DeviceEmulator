from lewis.adapters.stream import StreamAdapter, Cmd


class AG33220AStreamInterface(StreamAdapter):

    commands = {
        Cmd("get_voltage", "^VOLT\?$"),
        Cmd("set_voltage", "^VOLT " + "([\-0-9.]+|MAX|MIN)$", argument_mappings=[str]),
        Cmd("get_freq", "^FREQ\?$"),
        Cmd("set_freq", "^FREQ " + "([\-0-9.]+|MAX|MIN)$", argument_mappings=[str]),
        Cmd("get_offset", "^VOLT:OFFS\?$"),
        Cmd("set_offset", "^VOLT:OFFS " + "([\-0-9.]+)$", argument_mappings=[float]),
        Cmd("get_units", "^VOLT:UNIT\?$"),
        Cmd("set_units", "^VOLT:UNIT " + "(VPP|VRMS|DBM)$", argument_mappings=[str]),
        Cmd("get_function", "^FUNC\?$"),
        Cmd("set_function", "^FUNC " + "(SIN|SQU|RAMP|PULS|NOIS|DC|USER)$", argument_mappings=[str]),
        Cmd("get_output", "^OUTP\?$"),
        Cmd("set_output", "^OUTP " + "(0|1|ON|OFF)$", argument_mappings=[str]),
        Cmd("get_idn", "^\*IDN\?$"),
        Cmd("get_voltage_high", "^VOLT:HIGH\?$"),
        Cmd("set_voltage_high", "^VOLT:HIGH" + "([\-0-9.]+)$", argument_mappings=[float]),
        Cmd("get_voltage_low", "^VOLT:LOW\?$"),
        Cmd("set_voltage_low", "^VOLT:LOW" + "([\-0-9.]+)$", argument_mappings=[float]),
    }

    in_terminator = "\n"    # \r\n for putty
    out_terminator = "\n"

    # Takes in a value and returns a value in the form of x.xxxxxxxxxxxxxEYY
    def float_output(self, value):
        value = float('%s' % float('%.4g' % float(value)))
        return "{:+.13E}".format(value)

    # If the value is above or below the upper or lower bound
    # then the upper or lower bound will be returned respectively
    # otherwise the value is returned
    def limit(self,value,upper_bound,lower_bound):
        if value >= upper_bound:
            return upper_bound
        elif value < lower_bound:
            return lower_bound
        else:
            return value

    def get_voltage(self):
        return self.float_output(self._device.voltage)

    def set_voltage(self, new_voltage):
        try:
            self._device.voltage = self.limit(float(new_voltage), 10, 0.01)
        except:
            self._device.voltage = {"MIN": 0.01, "MAX": 10}[new_voltage]

    def get_freq(self):
        return self.float_output(self._device.frequency)

    def set_freq(self, new_frequency):
        lower_bound = {"SIN": 10**-6, "SQU": 10**-6, "RAMP": 10**-6, "PULS": 5*10**-4, "NOIS": 1*10**-6, "USER": 10**-6}[self._device.function]
        upper_bound = {"SIN": 2*10**7, "SQU": 2*10**7, "RAMP": 2*10**5, "PULS": 5*10**6, "NOIS": 2*10**7, "USER": 6*10**6}[self._device.function]
        try:
            self._device.frequency = self.limit(float(new_frequency), upper_bound, lower_bound)
        except:
            self._device.frequency = {"MIN": lower_bound, "MAX": upper_bound}[new_frequency]

    def get_offset(self):
        return self.float_output(self._device.offset)

    def set_offset(self, new_offset):
        self._device.offset = new_offset

    def get_units(self):
        return self._device.units

    def set_units(self, new_units):
        self._device.units = new_units

    def get_function(self):
        return self._device.function

    def set_function(self, new_function):
        print(new_function,"\n",self._device.function)
        self._device.function = new_function
        self.set_freq(self._device.frequency)
        print(new_function, "\n\n", self._device.function)

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

    def get_voltage_high(self):
        return self.float_output(self._device.voltageHigh)

    def set_voltage_high(self, new_voltage_high):
        self._device.voltageHigh = new_voltage_high

    def get_voltage_low(self):
        return self.float_output(self._device.voltageLow)

    def set_voltage_low(self, new_voltage_low):
        self._device.voltageLow = new_voltage_low

    def handle_error(self, request, error):
        print(str(error))

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
