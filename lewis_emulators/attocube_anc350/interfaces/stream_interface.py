from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log
from lewis_emulators.utils.byte_conversions import int_to_raw_bytes, raw_bytes_to_int
from functools import partial

BYTES_IN_INT = 4

convert_to_response = partial(int_to_raw_bytes, length=BYTES_IN_INT, low_byte_first=True)

# NB, all variables used from here onwards are named the same in the C driver

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

#  Memory addresses
ID_ANC_AMPL = 0x400
ID_ANC_FAST_FREQ = 0x0401
ID_ANC_STATUS = 0x0404
ID_ANC_REFCOUNTER = 0x0407  # The position of home
ID_ANC_COUNTER = 0x0415
ID_ANC_UNIT = 0x041D
ID_ANC_SENSOR_VOLT = 0x0526
ID_ANC_REGSPD_SETP = 0x0542  # Speed of the controller
ID_ANC_REGSPD_SETPS = 0x0549  # Step width of the controller
ID_ANC_MAX_AMP = 0x054F
ID_ANC_CAP_VALUE = 0x0569


# Status bitmask
ANC_STATUS_RUNNING = 0x0001
ANC_STATUS_HUMP = 0x0002
ANC_STATUS_SENS_ERR = 0x0100
ANC_STATUS_DISCONN = 0x0400
ANC_STATUS_REF_VALID = 0x0800
ANC_STATUS_ENABLE = 0x1000


@has_log
class AttocubeANC350StreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation. Match anything!
    commands = {
        Cmd("any_command", "^([\s\S]*)$"),
    }

    in_terminator = ""
    out_terminator = ""

    # Due to poll rate of the driver this will get individual commands
    readtimeout = 10

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    def any_command(self, command):
        length = raw_bytes_to_int(command[:BYTES_IN_INT])

        try:
            opcode, address, index, correlation_num = [raw_bytes_to_int(command[x:x + BYTES_IN_INT])
                                                   for x in range(BYTES_IN_INT, length + 1, BYTES_IN_INT)]
        except:
            print("Error splitting")
            print "Command was {}".format(command)
            print("Length was {}".format(length))

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
        print("GOT SET!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def get(self, address, index, correlation_num):
        command_mapping = {
            ID_ANC_COUNTER: self.get_position(index),
            ID_ANC_REFCOUNTER: 0,
            ID_ANC_STATUS: self.get_status(index),
            ID_ANC_UNIT: self.get_unit(index),
            ID_ANC_REGSPD_SETP: self.get_speed(index),
            ID_ANC_SENSOR_VOLT: 2000,
            ID_ANC_MAX_AMP: 60000,
            ID_ANC_AMPL: 30000,
            ID_ANC_FAST_FREQ: 1000,

        }
        print("Getting address " + hex(address))
        try:
            data = command_mapping[address]
        except KeyError:
            data = 0  # Just return 0 for now
        int_responses = [UC_ACK, address, index, correlation_num, UC_REASON_OK, data]
        print("Responding with {}".format(int_responses))
        response = "".join(convert_to_response(x) for x in int_responses)
        return_length = len(response)
        return convert_to_response(return_length) + response

    def get_position(self, index):
        return 500

    def get_speed(self, index):
        return 10

    def get_unit(self, index):
        return 0x00

    def get_status(self, index):
        # For now just respond with all ok
        return ANC_STATUS_REF_VALID + ANC_STATUS_ENABLE
