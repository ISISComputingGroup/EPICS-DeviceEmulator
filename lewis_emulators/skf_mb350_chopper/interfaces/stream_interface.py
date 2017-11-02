from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log

from crc16 import crc16_matches


class SkfMb350ChopperStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation. Match anything!
    commands = {
        Cmd("any_command", "^([\s\S]*)$"),
    }

    in_terminator = "[terminator]"
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
            0xC0: self.get_phase_info,
        }

        address = ord(command[0])
        if not 0 <= address < 16:
            raise ValueError("Address should be in range 0-15")

        # Constant function code. Should always be 0x80
        function_code = ord(command[1])
        if function_code != 0x80:
            raise ValueError("Function code should always be 0x80")

        command_number = ord(command[2])
        if command_number not in command_mapping.keys():
            raise ValueError("Command number should be in map")

        command_data = [ord(c) for c in command[3:-2]]

        crc = [ord(c) for c in command[-2:]]

        if not crc16_matches(command[:-2], crc):
            raise ValueError("CRC Checksum didn't match")

        return command_mapping[command_number](address, command_data)

    def start(self, address, data):
        self._device.start(address)

    def stop(self, address, data):
        self._device.stop(address)

    @has_log
    def set_rotational_speed(self, address, data):
        self.log.info("Setting rotational speed")
        self.log.info("Address = {}".format(address))
        self.log.info("Data = {}".format(data))

        byte = 2**8
        nominal_phase = (byte**3)*data[0] + (byte**2)*data[1] + byte*data[2] + data[3]
        self.log.info("Setting nominal phase to {}".format(nominal_phase))
        self._device.set_nominal_phase(address, nominal_phase)

    @has_log
    def get_phase_info(self, address, data):
        self.log.info("Getting phase info")
        self.log.info("Address = {}".format(address))

        phase = self._device.get_phase(address)
        self.log.info("Returning phase as {}".format(phase))
        return phase
