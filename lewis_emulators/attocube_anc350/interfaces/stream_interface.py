from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log
from lewis_emulators.utils.byte_conversions import int_to_raw_bytes, raw_bytes_to_int
from functools import partial


UC_SET = 0  # Set command
UC_GET = 1  # Get command
UC_ACK = 3  # Ack command
UC_TELL = 4  # Event command

UC_REASON_OK = 0  # All ok
UC_REASON_ADDR = 1  # Invalid address
UC_REASON_RANGE = 2  # Value out of range
UC_REASON_IGNORED = 3  # Telegram was ignored
UC_REASON_VERIFY = 4  # Verify of data failed
UC_REASON_TYPE = 5  # Wrong type of data
UC_REASON_UNKNW = 99  # unknown error

BYTES_IN_INT = 4

convert_to_response = partial(int_to_raw_bytes, length=BYTES_IN_INT, low_byte_first=True)

@has_log
class AttocubeANC350StreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation. Match anything!
    commands = {
        Cmd("any_command", "^(.*)$"),
    }

    in_terminator = ""
    out_terminator = ""

    # Due to poll rate of the driver this will get individual commands
    readtimeout = 10

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    def any_command(self, command):
        length, opcode, address, index, correlation_num = [raw_bytes_to_int(command[x:x + BYTES_IN_INT])
                                                           for x in range(0, len(command), BYTES_IN_INT)]

        # Length should describe command minus itself
        actual_length = len(command) - BYTES_IN_INT
        if actual_length != length:
            raise ValueError("Told I would receive {} bytes but received {}".format(len(command) - BYTES_IN_INT))

        if opcode > 4:
            raise ValueError("Unrecognised opcode {}".format(opcode))

        command_mapping = {
            UC_GET: self.get,
            UC_SET: self.set,
        }

        return command_mapping[opcode](address, index, correlation_num)

    def set(self, address, index, correlation_num):
        pass

    def get(self, address, index, correlation_num):
        print("Getting address " + hex(address))
        int_responses = [UC_ACK, address, index, correlation_num, UC_REASON_OK, 252]
        response = "".join(convert_to_response(x) for x in int_responses)
        return_length = len(response)
        print("Responding with {}".format(convert_to_response(return_length) + response))
        return convert_to_response(return_length) + response
