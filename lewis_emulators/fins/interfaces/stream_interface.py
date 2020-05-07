from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log

from lewis_emulators.utils.byte_conversions import raw_bytes_to_int
from response_utilities import phase_time_response_packet, general_status_response_packet, check_is_byte, \
    dm_memory_area_read_response_fins_frame
from ..device import SimulatedFinsPLC


@has_log
class FinsPLCStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation. Match anything!
    commands = {
        Cmd("any_command", "^([\s\S]*)$"),
    }

    in_terminator = "\r\n"
    out_terminator = in_terminator

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    def any_command(self, command):
        """
        Handles all command sent to this emulator. It checks the validity of the command, and raises an error if it
        finds something invalid. If the command is valid, then it returns a string representing the response to the
        command.
        :param command: A string where every character represents a byte from the received FINS command frame.
        :return: a string where each character represents a
        byte from the FINS response frame.
        """
        self._check_fins_frame_header_validity(command[:10])

        # We extract information necessary for building the FINS response header
        self.device.network_address = ord(command[3])
        self.log.info("Server network address: {}".format(self.device.network_address))

        self.device.unit_address = ord(command[5])
        self.log.info("Server Unit address: {}".format(self.device.unit_address))

        client_network_address = ord(command[6])
        self.log.info("Client network address: {}".format(client_network_address))

        client_node_address = ord(command[7])
        self.log.info("Client node address: {}".format(client_node_address))

        client_unit_address = ord(command[8])
        self.log.info("Client unit address: {}".format(client_unit_address))

        service_id = ord(command[9])
        self.log.info("Service id: {}".format(service_id))

        if ord(command[10]) != 0x01 or ord(command[11]) != 0x01:
            raise ValueError("The command code should be 0x0101, for memory area read command!")

        if ord(command[12]) != 0x82:
            raise ValueError("The emulator only supports reading words from the DM area, for which the code is 82.")

        # the address of the starting word from where reading is done. Addresses are stored in two bytes.
        memory_start_address = raw_bytes_to_int(command[13:15])

        # The FINS PLC supports reading either a certain number of words, or can also read individual bits in a word.
        # The helium recovery memory map implies that that PLC uses word designated reading. When bit designated
        # reading is not used, the 16th byte of the command is 0x00.
        if ord(command[15]) != 0x00:
            raise ValueError("The emulator only supports word designated memory reading. The bit address must be 0x00")

        number_of_words_to_read = raw_bytes_to_int(command[16:18])

        # The helium recovery PLC memory map has addresses that store types that take up either one word (16 bits) or
        # two. Most take up one word, so if the number of words to read is two we check that the client wants to read
        # from a memory location from where a 32 bit value starts.
        if number_of_words_to_read == 2 and memory_start_address not in self.device.double_word_memory_locations:
            raise ValueError("The memory start address specified corresponds to a single word in the memory map, "
                             "not two.")
        elif number_of_words_to_read > 2:
            raise ValueError("The memory map only specifies data types that should take up two words at most.")

        return dm_memory_area_read_response_fins_frame(self.device.server_network_address,
                                                       self.device.server_unit_address, client_network_address,
                                                       client_node_address, client_unit_address, service_id,
                                                       memory_start_address, number_of_words_to_read)

    @staticmethod
    def _check_fins_frame_header_validity(fins_frame_header):
        """
        Checks that the FINS frame header part of the command is valid for a command sent from a client to a server
        (PLC).
        :param fins_frame_header: A string where every character represents a byte from the received FINS frame header.
        :return: None
        """

        # ICF means Information Control Field, it gives information about if the frame is for a command or a response,
        # and if a response is needed or not.
        icf = ord(fins_frame_header[0])
        if icf != 0x80:
            raise ValueError("ICF value should always be 0x80 for a command sent to the emulator")

        # Reserved byte. Should always be 0x00
        if ord(fins_frame_header[1]) != 0x00:
            raise ValueError("Reserved byte should always be 0x00.")

        if ord(fins_frame_header[2]) != 0x02:
            raise ValueError("Gate count should always be 0x02.")

        check_is_byte(fins_frame_header[3])

        if ord(fins_frame_header[4]) != SimulatedFinsPLC.FINS_HE_RECOVERY_NODE:
            raise ValueError("The node address of the FINS helium recovery PLC should be {}!".format(
                SimulatedFinsPLC.FINS_HE_RECOVERY_NODE))

        for i in range(5, 10):
            check_is_byte(fins_frame_header[i])
