from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log

from byte_conversions import raw_bytes_to_int
from response_utilities import Responses
from .crc16 import crc16_matches


class SkfMb350ChopperStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation. Match anything!
    commands = {
        Cmd("any_command", "^([\s\S]*)$"),
    }

    in_terminator = "[terminator]" + str(chr(0x0)) * 16
    out_terminator = in_terminator

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    @has_log
    def any_command(self, command):

        command_mapping = {
            0x20: self.start,
            0x30: self.stop,
            0x60: self.set_rotational_speed,
            0x90: self.set_nominal_phase,
            0xC0: self.get_phase_info,
        }

        address = ord(command[0])
        if not 0 <= address < 16:
            raise ValueError("Address should be in range 0-15")

        # Constant function code. Should always be 0x80
        if ord(command[1]) != 0x80:
            raise ValueError("Function code should always be 0x80")

        command_number = ord(command[2])
        if command_number not in command_mapping.keys():
            raise ValueError("Command number should be in map")

        command_data = [c for c in command[3:-2]]

        crc = [ord(c) for c in command[-2:]]

        if not crc16_matches(command[:-2], crc):
            raise ValueError("CRC Checksum didn't match")

        return command_mapping[command_number](address, command_data)

    def start(self, address, data):
        self._device.start()

    def stop(self, address, data):
        self._device.stop()

    @has_log
    def set_nominal_phase(self, address, data):
        self.log.info("Setting phase")
        self.log.info("Data = {}".format(data))
        nominal_phase = raw_bytes_to_int(data) / 1000.
        self.log.info("Setting nominal phase to {}".format(nominal_phase))
        self._device.set_nominal_phase(nominal_phase)

    @has_log
    def set_rotational_speed(self, address, data):
        self.log.info("Setting frequency")
        self.log.info("Data = {}".format(data))
        freq = raw_bytes_to_int(data)
        self.log.info("Setting frequency to {}".format(freq))
        self._device.set_frequency(freq)

    @has_log
    def get_phase_info(self, address, data):
        self.log.info("Getting phase info")
        response = Responses.phase_information_response_packet(address, self._device)
        self.log.info("Response is: {}".format(response))
        return response
