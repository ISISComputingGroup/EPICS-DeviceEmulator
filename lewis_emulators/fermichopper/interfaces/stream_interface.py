from lewis.adapters.stream import StreamAdapter, Cmd

import math


class JulichChecksum(object):
    @staticmethod
    def _hex_value(char):
        """
        Converts an uppercase octadecimal character or a hash to it's ASCII identifier.

        :param char: The character to convert
        :return: the ascii code of the given character
        """
        assert char in list("#0123456789ABCDEFGH"), "Invalid character - can't calculate hex value!"
        return ord(char)

    @staticmethod
    def _calculate(alldata):
        """
        Calculates the Julich checksum of the given data
        :param alldata: the input data (list of chars, length 5)
        :return: the Julich checksum of the given input data
        """
        return "00" if all(x in ['0', '#'] for x in alldata) else hex(sum(JulichChecksum._hex_value(i) for i in alldata)).upper()[-2:]

    @staticmethod
    def verify(header, data, actual_checksum):
        """
        Verifies that the checksum of received data is correct.
        :param header: The leading # and the first byte (str, length 2)
        :param data: The data bytes (str, length 4)
        :param actual_checksum: The transmitted checksum (str, length 2)
        :return: Nothing
        :raises: AssertionError: If the checksum didn't match or the inputs were invalid
        """
        assert len(header) == 2, "Header should have length 2"
        assert len(data) == 4, "Data should have length 4"
        assert len(actual_checksum) == 2, "Actual checksum should have length 2"
        assert JulichChecksum._calculate(list(header) + list(data)) == actual_checksum, "Checksum did not match"

    @staticmethod
    def append_checksum(data):
        """
        Utility method for appending the Julich checksum to the input data
        :param data: the input data
        :return: the input data with it's checksum appended
        """
        assert len(data) == 6, "Unexpected data length."
        return data + JulichChecksum._calculate(data)


class FermichopperStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_all_data", "^#00000([0-9A-F]{2})\$$"),
        Cmd("execute_command", "^#1([0-9A-F]{4})([0-9A-F]{2})\$$"),
        Cmd("set_speed", "^#3([0-9A-F]{4})([0-9A-F]{2})\$$"),
        Cmd("set_delay_highword", "^#6([0-9A-F]{4})([0-9A-F]{2})\$$"),
        Cmd("set_delay_lowword", "^#5([0-9A-F]{4})([0-9A-F]{2})\$$"),
        Cmd("set_gate_width", "^#9([0-9A-F]{4})([0-9A-F]{2})\$$"),
        # Cmd("catch_all", "^#9.*$"), # Catch-all command for debugging
    }

    in_terminator = "\n"
    out_terminator = "\n"

    # Catch all command for debugging if the IOC sends strange characters in the checksum.
    # def catch_all(self):
    #    pass

    def build_status_code(self):
        status = 0

        if True:
            status += 1
        if self._device.get_true_speed() == self._device.get_speed_setpoint():
            status += 2
        if self._device.magneticbearing:
            status += 8
        if self._device.get_voltage() > 0:
            status += 16
        if self._device.speed > 600:
            status += 1024
        if self._device.speed > 10 and not self._device.magneticbearing:
            status += 2048

        return status

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_all_data(self, checksum):
        JulichChecksum.verify('#0', '0000', checksum)
        return JulichChecksum.append_checksum('#1' + self._device.get_last_command()) \
                + JulichChecksum.append_checksum("#2{:04X}".format(self.build_status_code())) \
                + JulichChecksum.append_checksum("#3000{:01X}".format(12 - (self._device.get_speed_setpoint()/50))) \
                + JulichChecksum.append_checksum("#4{:04X}".format(self._device.get_true_speed()*60)) \
                + JulichChecksum.append_checksum("#5{:04X}".format(int(math.floor((self._device.delay * 50.4) % 65536)))) \
                + JulichChecksum.append_checksum("#6{:04X}".format(int(math.floor((self._device.delay * 50.4) / 65536)))) \
                + JulichChecksum.append_checksum("#75209") \
                + JulichChecksum.append_checksum("#80000") \
                + JulichChecksum.append_checksum("#9{:04X}".format(int(math.floor(self._device.get_gate_width() * 50.4)))) \
                + JulichChecksum.append_checksum("#A{:04X}".format(int(round(self._device.get_current() / 0.002016)))) \
                + JulichChecksum.append_checksum("#B{:04X}".format(int(round((self._device.autozero_1_upper + 22.86647) / 0.04486)))) \
                + JulichChecksum.append_checksum("#C{:04X}".format(int(round((self._device.autozero_2_upper + 22.86647) / 0.04486)))) \
                + JulichChecksum.append_checksum("#D{:04X}".format(int(round((self._device.autozero_1_lower + 22.86647) / 0.04486)))) \
                + JulichChecksum.append_checksum("#E{:04X}".format(int(round((self._device.autozero_2_lower + 22.86647) / 0.04486)))) \
                + JulichChecksum.append_checksum("#F{:04X}".format(int(round(self._device.get_voltage() / 0.4274)))) \
                + JulichChecksum.append_checksum("#G{:04X}".format(int(round((self._device.get_electronics_temp()+25.0) / 0.14663)))) \
                + JulichChecksum.append_checksum("#H{:04X}".format(int(round((self._device.get_motor_temp()+12.124) / 0.1263))))

    def execute_command(self, command, checksum):
        JulichChecksum.verify('#1', command, checksum)

        valid_commands = ["0001", "0002", "0003", "0004", "0005"]

        assert command in valid_commands, "Invalid command."

        self._device.do_command(command)

    def set_speed(self, command, checksum):
        JulichChecksum.verify("#3", command, checksum)
        self._device.set_speed_setpoint((12-int(command, 16))*50)

    def set_delay_lowword(self, command, checksum):
        JulichChecksum.verify('#5', command, checksum)
        self._device.set_delay_lowword(int(command, 16))

    def set_delay_highword(self, command, checksum):
        JulichChecksum.verify('#6', command, checksum)
        self._device.set_delay_highword(int(command, 16))

    def set_gate_width(self, command, checksum):
        JulichChecksum.verify('#9', command, checksum)
        self._device.set_gate_width(int(command, 16) / 50.4)