from lewis.devices import Device


class SimulatedAG33220A(Device):
    make = "Agilent Technologies,33220A"
    firmware_rev_num = "MY44033103,2.02"
    boot_kernel_revision_number = "2.02"
    asic_rev_num = "22"
    printed_circuit_board_rev_num = "2"
    idn = make+"-"+firmware_rev_num+"-"+boot_kernel_revision_number+"-"+asic_rev_num+"-"+printed_circuit_board_rev_num
    amplitude = 0.1
    frequency = 1000
    offset = 0
    units = "VPP"
    function = "SIN"
    output = 0
    voltage_high = 0.05
    voltage_low = -0.05
    amplitude_lower_bound = 0.01
    amplitude_upper_bound = 10
    offset_lower_bound = -4.995
    offset_upper_bound = 4.995
    voltage_lower_bound = -5
    voltage_upper_bound = 5
    voltage_low_lower_bound = -5
    voltage_low_upper_bound = 4.99
    voltage_high_lower_bound = -4.99
    voltage_high_upper_bound = 5
    voltage_precision = 0.01




    def limit_or_min_max(self, value, minimum, maximum):
        try:
            return self.limit(float(value), minimum, maximum)
        except:
            return {"MIN": minimum, "MAX": maximum}[value]

    # If the value is above or below the upper or lower bound
    # then the upper or lower bound will be returned respectively
    # otherwise the value is returned
    def limit(self, value, lower_bound, upper_bound):
        if value >= upper_bound:
            return upper_bound
        elif value < lower_bound:
            return lower_bound
        else:
            return value

    def set_new_amplitude(self, new_amplitude):
        new_amplitude = self.limit_or_min_max(new_amplitude, self.amplitude_lower_bound, self.amplitude_upper_bound)
        if 0.5 * new_amplitude + self.offset > self.voltage_upper_bound or self.offset - 0.5 * new_amplitude < self.voltage_lower_bound:
            if 0.5 * new_amplitude + self.offset > self.voltage_upper_bound:
                offset_difference = 0.5 * new_amplitude + self.offset - self.voltage_upper_bound
            elif self.offset - 0.5 * new_amplitude < self.voltage_lower_bound:
                offset_difference = -0.5 * new_amplitude + self.offset + self.voltage_upper_bound
            self.offset -= offset_difference
            self.voltage_high -= offset_difference
            self.voltage_low -= offset_difference
        else:
            self.update_volt_high_and_low(new_amplitude, self.offset)
        self.amplitude = new_amplitude

    def set_new_frequency(self, new_frequency):
        self.frequency = self.limit_or_min_max(new_frequency, self.frequency_lower_bound(), self.frequency_upper_bound())

    def set_new_voltage_high(self,new_voltage_high):
        new_voltage_high = self.limit(new_voltage_high, self.voltage_high_lower_bound, self.voltage_high_upper_bound)
        if new_voltage_high <= self.voltage_low:
            self.voltage_low = self.limit(new_voltage_high - self.voltage_precision, self.voltage_low_lower_bound, new_voltage_high)
        self.update_volt_and_offs(self.voltage_low, new_voltage_high)

    def set_new_voltage_low(self,new_voltage_low):
        new_voltage_low = self.limit(new_voltage_low, self.voltage_low_lower_bound, self.voltage_low_upper_bound)
        if new_voltage_low >= self.voltage_high:
            self.set_voltage_high(self.limit(new_voltage_low + self.voltage_precision, new_voltage_low, self.voltage_high_upper_bound))
        self.update_volt_and_offs(new_voltage_low, self.voltage_high)

    def update_volt_and_offs(self, new_low, new_high):
        self.voltage_high = new_high
        self.voltage_low = new_low
        self.amplitude = self.voltage_high-self.voltage_low
        self.offset = (self.voltage_high+self.voltage_low)/2

    def set_offs_and_update_voltage(self, new_offset):
        new_offset = self.limit_or_min_max(new_offset, self.offset_lower_bound, self.offset_upper_bound)
        if new_offset+self.voltage_high > self.voltage_upper_bound:
            self.amplitude = 2/(self.voltage_upper_bound-new_offset)
            self.voltage_high = self.voltage_upper_bound
            self.voltage_low = self.voltage_upper_bound - self.amplitude
        elif new_offset+self.voltage_low < self.voltage_lower_bound:
            self.amplitude = 2/(self.voltage_lower_bound-new_offset)
            self.voltage_low = self.voltage_lower_bound
            self.voltage_high = self.voltage_lower_bound + self.amplitude
        else:
            self.update_volt_high_and_low(self.amplitude, new_offset)
        self.offset = new_offset

    def update_volt_high_and_low(self, new_volt, new_offs):
        self.offset = new_offs
        self.amplitude = new_volt
        self.voltage_high = new_offs + new_volt / 2
        self.voltage_low = new_offs - new_volt / 2

    def frequency_lower_bound(self):
        return {"SIN": 10 ** -6, "SQU": 10 ** -6, "RAMP": 10 ** -6, "PULS": 5 * 10 ** -4, "NOIS": 1 * 10 ** -6, "USER": 10 ** -6}[self.function]

    def frequency_upper_bound(self):
        return {"SIN": 2 * 10 ** 7, "SQU": 2 * 10 ** 7, "RAMP": 2 * 10 ** 5, "PULS": 5 * 10 ** 6, "NOIS": 2 * 10 ** 7,"USER": 6 * 10 ** 6}[self.function]

    pass
