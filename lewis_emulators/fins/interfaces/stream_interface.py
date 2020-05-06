from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log

from lewis_emulators.utils.byte_conversions import raw_bytes_to_int
from response_utilities import phase_time_response_packet, general_status_response_packet, check_is_byte, \
    dm_memory_area_read_response_fins_frame


@has_log
class FinsPLCStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation. Match anything!
    commands = {
        Cmd("any_command", "^([\s\S]*)$"),
    }

    in_terminator = "\r\n"
    out_terminator = in_terminator

    memory_value_mapping = {
        19500: 1,  # heartbeat
        19533: 999,  # helium purity
        19534: 2136,  # dew point
        19900: 245  # HE_BAG_PR_BE_ATM
    }

    double_word_memory_locations = {}

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    def any_command(self, command):

        icf = ord(command[0])
        if icf != 0x80:
            raise ValueError("ICF value should always be 0x80 for a command sent to the emulator")

        # Reserved byte. Should always be 0x00
        if ord(command[1]) != 0x00:
            raise ValueError("Reserved byte should always be 0x00.")

        if ord(command[2]) != 0x02:
            raise ValueError("Gate count should always be 0x02.")

        check_is_byte(command[3])
        self.device.network_address = ord(command[3])
        self.log.info("Server network address: {}".format(self.device.network_address))

        if ord(command[4]) != 0x3A:
            raise ValueError("The node address of the FINS helium recovery PLC should be 58!")

        check_is_byte(command[5])
        self.device.unit_address = ord(command[5])
        self.log.info("Server Unit address: {}".format(self.device.unit_address))

        check_is_byte(command[6])
        client_network_address = ord(command[6])
        self.log.info("Client network address: {}".format(client_network_address))

        check_is_byte(command[7])
        client_node_address = ord(command[7])
        self.log.info("Client node address: {}".format(client_node_address))

        check_is_byte(command[8])
        client_unit_address = ord(command[8])
        self.log.info("Client unit address: {}".format(client_unit_address))

        check_is_byte(command[9])
        service_id = ord(command[9])
        self.log.info("Service id: {}".format(service_id))

        if ord(command[10]) != 0x01 and ord(command[11]) != 0x01:
            raise ValueError("The command code should be 0x0101, for memory area read command!")

        if ord(command[12]) != 0x82:
            raise ValueError("The emulator only supports reading words from the DM area, for which the code is 82.")

        memory_start_address = raw_bytes_to_int(command[13:15])

        if ord(command[15]) != 0x00:
            raise ValueError("The emulator only supports word designated memory reading. The bit address must be 0x00")

        number_of_words_to_read = raw_bytes_to_int(command[16:18])

        if number_of_words_to_read == 2 and memory_start_address not in self.double_word_memory_locations:
            raise ValueError("The memory start address specified corresponds to a single word in the memory map, "
                             "not two.")
        elif number_of_words_to_read > 2:
            raise ValueError("The memory map only specifies data types that should take up two words at most.")

        return dm_memory_area_read_response_fins_frame(self.device.server_network_address,
                                                       self.device.server_unit_address, client_network_address,
                                                       client_node_address, client_unit_address, service_id,
                                                       memory_start_address, number_of_words_to_read)

    def get_phase_info(self, address, data):
        self.log.info("Getting phase info")
        return phase_information_response_packet(address, self._device)
