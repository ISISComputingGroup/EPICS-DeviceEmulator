from lewis.adapters.stream import StreamAdapter, Cmd


class JulichChecksum(object):
    @staticmethod
    def _hex_value(char):
        """
        Converts an uppercase hexed character to it's ASCII identifier
        :param char: The character to convert
        :return: the ascii code of the given character
        """
        assert char in list("0123456789ABCDEF"), "Invalid character - can't calculate hex value!"
        return ord(char)

    @staticmethod
    def calculate(data):
        """
        Calculates the Julich checksum of the given data
        :param data: the input data (list of chars, length 5)
        :return: the Julich checksum of the given input data
        """
        assert len(data) == 5, "Unexpected data length."
        return "00" if all(x == '0' for x in data) else hex(sum(JulichChecksum._hex_value(i) for i in data)).upper()[-2:]

    @staticmethod
    def verify(initialbyte, data, actual_checksum):
        """
        Verifies that the checksum of received data is correct.
        :param initialbyte: The first byte (str, length 1)
        :param data: The data bytes (str, length 4)
        :param actual_checksum: The transmitted checksum (str, length 2)
        :return: Nothing
        :raises: AssertionError: If the checksum didn't match or the inputs were invalid
        """
        assert len(initialbyte) == 1, "Initial byte should have length 1"
        assert len(data) == 4, "Data should have length 4"
        assert len(actual_checksum) == 2, "Actual checksum should have length 2"
        assert JulichChecksum.calculate([initialbyte] + list(data)) == actual_checksum, "Checksum did not match"

    @staticmethod
    def append_checksum(data):
        """
        Utility method for appending the Julich checksum to the input data
        :param data: the input data
        :return: the input data with it's checksum appended
        """
        return data + JulichChecksum.calculate(data)


class FermichopperStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_all_data", "^#00000([0-9A-F]{2})\$$"),
        Cmd("execute_command", "^#1([0-9A-F]{4})([0-9A-F]{2})\$$"),
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_all_data(self, checksum):
        JulichChecksum.verify('0', '0000', checksum)
        return "#" + JulichChecksum.append_checksum('1' + self._device.get_last_command())

    def execute_command(self, command, checksum):
        JulichChecksum.verify('1', command, checksum)

        valid_commands = ["0001", "0002", "0003", "0006", "0007"]

        assert command in valid_commands, "Invalid command."

        self._device.set_last_command(command)

