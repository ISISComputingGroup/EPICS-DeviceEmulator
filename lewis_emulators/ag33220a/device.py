from lewis.devices import Device


class SimulatedAG33220A(Device):
    """
    Simulated AG33220A
    """
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

    def limit(self, value, minimum, maximum):
        """
        Limits an input number between two given numbers
        or sets the value to the maximum or minimum.

        :param value: the value to be limited
        :param minimum: the smallest that the value can be
        :param maximum: the largest that the value can be

        :return: the value after it has been limited
        """
        try:
            value = float(value)
            if value >= maximum:
                return maximum
            elif value < minimum:
                return minimum
            else:
                return value
        except:
            return {"MIN": minimum, "MAX": maximum}[value]

    def set_new_amplitude(self, new_amplitude):
        """
        Changing the amplitude to the new amplitude whilst also changing
        voltage high, voltage low, and offset if voltage high or low is outside the boundary.

        :param new_amplitude; the amplitude to set the devices amplitude to
        """
        new_amplitude = self.limit(new_amplitude, self.amplitude_lower_bound, self.amplitude_upper_bound)
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
        """
        Sets the frequency within limits between upper and lower bound
        which are different for each function.

        :param new_frequency: the frequency which wants to be set
        """
        self.frequency = self.limit(new_frequency, self.frequency_lower_bound(), self.frequency_upper_bound())

    def set_new_voltage_high(self,new_voltage_high):
        """
        Sets a new voltage high which then changes the voltage low if voltage high
        is set to a value lower than the voltage low.
        The voltage offset and amplitude are then updated.

        :param new_voltage_high: the value of voltage high which is to be set
        """
        new_voltage_high = self.limit(new_voltage_high, self.voltage_high_lower_bound, self.voltage_high_upper_bound)
        if new_voltage_high <= self.voltage_low:
            self.voltage_low = self.limit(new_voltage_high - self.voltage_precision, self.voltage_low_lower_bound, new_voltage_high)
        self.update_volt_and_offs(self.voltage_low, new_voltage_high)

    def set_new_voltage_low(self,new_voltage_low):
        """
        Sets a new voltage low which then changes the voltage high if voltage low
        is set to a value higher than the voltage high.
        The voltage offset and amplitude are then updated.

        :param new_voltage_low: the value of voltage low which is to be set
        """
        new_voltage_low = self.limit(new_voltage_low, self.voltage_low_lower_bound, self.voltage_low_upper_bound)
        if new_voltage_low >= self.voltage_high:
            self.voltage_high = self.limit(new_voltage_low + self.voltage_precision, new_voltage_low, self.voltage_high_upper_bound)
        self.update_volt_and_offs(new_voltage_low, self.voltage_high)

    def update_volt_and_offs(self, new_low, new_high):
        """
        Updates the value of amplitude and offset if there is a change in
        voltage low or voltage high.

        :param new_low: the value of voltage low
        :param new_high: the value of voltage high
        """
        self.voltage_high = new_high
        self.voltage_low = new_low
        self.amplitude = self.voltage_high-self.voltage_low
        self.offset = (self.voltage_high+self.voltage_low)/2

    def set_offs_and_update_voltage(self, new_offset):
        """
        Sets the value of offset and updates the amplitude, voltage low and
        voltage high for a new value of the offset.

        :param new_offset: the new offset to be set
        """
        new_offset = self.limit(new_offset, self.offset_lower_bound, self.offset_upper_bound)
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
        """
        Updates the value of voltage high and low for a given value of
        amplitude and offset.

        :param new_volt: the value of the amplitude
        :param new_offs: the value of the offset
        """
        self.offset = new_offs
        self.amplitude = new_volt
        self.voltage_high = new_offs + new_volt / 2
        self.voltage_low = new_offs - new_volt / 2

    def frequency_lower_bound(self):
        """
        Returning the appropriate lower bound for the frequency for a given function.

        :return: lower bound for the frequency for a given function
        """
        return {"SIN": 10 ** -6, "SQU": 10 ** -6, "RAMP": 10 ** -6, "PULS": 5 * 10 ** -4, "NOIS": 1 * 10 ** -6, "USER": 10 ** -6}[self.function]

    def frequency_upper_bound(self):
        """
            Returning the appropriate upper bound for the frequency for a given function.

            :return: upper bound for the frequency for a given function
        """
        return {"SIN": 2 * 10 ** 7, "SQU": 2 * 10 ** 7, "RAMP": 2 * 10 ** 5, "PULS": 5 * 10 ** 6, "NOIS": 2 * 10 ** 7,"USER": 6 * 10 ** 6}[self.function]

    pass
