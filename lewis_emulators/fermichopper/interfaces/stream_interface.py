from lewis.adapters.stream import StreamAdapter, Cmd


class JulichChecksum(object):
    @staticmethod
    def hex_value(char):
        if char == '0':
            return 0x30
        elif char == '1':
            return 0x31
        elif char == '2':
            return 0x32
        elif char == '3':
            return 0x33
        elif char == '4':
            return 0x34
        elif char == '5':
            return 0x35
        elif char == '6':
            return 0x36
        elif char == '7':
            return 0x37
        elif char == '8':
            return 0x38
        elif char == '9':
            return 0x39
        elif char == 'A':
            return 0x41
        elif char == 'B':
            return 0x42
        elif char == 'C':
            return 0x43
        elif char == 'D':
            return 0x44
        elif char == 'E':
            return 0x45
        elif char == 'F':
            return 0x46
        else:
            assert False, "Invalid character - can't calculate hex value!"

    @staticmethod
    def julich_checksum(initialbyte, data):
        assert len(initialbyte) == 1, "Checksum was called with more than one initial byte."
        assert len(data) == 4, "Checksum was called with more than four data bytes"

        alldata = list(data) + [initialbyte]

        if all(x == '0' for x in alldata):
            total = 0
        else:
            total = sum(JulichChecksum.hex_value(i) for i in alldata)

        return hex(total).upper()[2:]

    @staticmethod
    def verify_checksum(initialbyte, data, actual_checksum):
        assert JulichChecksum.julich_checksum(initialbyte, data) == actual_checksum, "Checksum did not match"


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
        # This is "known good" example data from the documentation.
        return "#10003F4"

    def execute_command(self, command, checksum):
        # This is "known good" example data from the documentation.
        print "Command was {command} and checksum was {checksum}".format(command=command, checksum=checksum)

        JulichChecksum.verify_checksum('1', command, checksum)

        return "#10003F4"

