from lewis_emulators.utils.byte_conversions import int_to_raw_bytes, float_to_raw_bytes, raw_bytes_to_int
from ..device import SimulatedFinsPLC


def check_is_byte(character):
    """
    Checks if the given character can represent a byte. Raises an error of it can not, otherwise returns nothing.
    :param character: A one character string.
    :return: None.
    """

    number = ord(character)
    if 0 > number > 255:
        raise ValueError("the character in the string must represent a byte value")


def dm_memory_area_read_response_fins_frame(device, client_network_address, client_node, client_unit_address,
                                            service_id, memory_start_address, number_of_words):
    """
    Returns a response to a DM memory area read command.

    Response structure is:
        10 bytes FINS frame header.
        2 bytes (integer): Command code, for memory area read in this case
        2 bytes (integer): End code. Shows errors.
        2 bytes for every word read.

    :param device: The Lewis device.
    :param client_network_address: The FINS network address of the client.
    :param client_node: The FINS node of the client.
    :param client_unit_address: The FINS unit address of the client.
    :param service_id: The service ID of the original command.
    :param memory_start_address: The memory address from where reading starts.
    :param number_of_words: The number of words to be read, starting from the start address, inclusive.
    :return: the response, represented as a string.
    """

    # The length argument asks for number of bytes, and each word has two bytes
    fins_reply = FinsResponseBuilder() \
        .add_fins_frame_header(device.network_address, device.unit_address, client_network_address,
                               client_node, client_unit_address, service_id) \
        .add_fins_command_and_error_codes()

    #  The plc has 2 byte words. The command asks for 1 word if the memory address stores a 16 bit integer, or 2 words
    #  if it stores a 32 bit integer, or a real number.
    if number_of_words == 1:
        fins_reply = fins_reply.add_int(device.int16_memory[memory_start_address], 2)

    #  The FINS driver does not recognise 32 bit ints. Instead, it represents 32 bit ints as an array of two 16 bit
    #  ints. Although the 16 bit ints are in big endian, in the array the first int is the least significant int, and
    #  the second one is the most significant one.
    elif number_of_words == 2:
        data = ""
        if memory_start_address in device.int32_memory.keys():
            # convert 32 bit int to array of two ints
            data = _convert_32bit_int_to_int16_array(device.int32_memory[memory_start_address])
        elif memory_start_address in device.float_memory.keys():
            # convert 32 bit int to array of two ints
            data = _convert_32bit_float_to_int16_array(device.float_memory[memory_start_address])

        fins_reply = fins_reply.add_int(data[0], 2).add_int(data[1], 2)
    elif number_of_words == 4:
        data = _convert_32bit_float_to_int16_array(device.float_memory[memory_start_address])
        fins_reply = fins_reply.add_int(data[0], 2).add_int(data[1], 2)

    return fins_reply.build()


def _convert_32bit_int_to_int16_array(number):
    """
    Converts a 32 bit integer into an array of two 16 bit integer. The first 16 bit integer is the least significant
    one, and the second is the most significant. The order of the 16 bit integers in the array is little endian.
    :param number: The number to be converted. But the individual 16 bit ints are encoded in big endian.
    :return: a list, with the first element being the least significant byte of the given number, and the second element
     being the most significant byte.
    """
    if type(number) != int:
        raise TypeError("number argument must always be an integer!")

    raw_bytes_representation = int_to_raw_bytes(number, 4, False)

    least_significant_byte = raw_bytes_to_int(raw_bytes_representation[2:4], low_bytes_first=False)
    most_significant_byte = raw_bytes_to_int(raw_bytes_representation[:2], low_bytes_first=False)

    return [least_significant_byte, most_significant_byte]


def _convert_32bit_float_to_int16_array(number):
    """
    Converts a 32 bit real number into an array of two 16 bit integer. The first 16 bit integer is the least significant
    one, and the second is the most significant. The order of the 16 bit integers in the array is little endian.
    :param number: The number to be converted. But the individual 16 bit ints are encoded in big endian.
    :return: a list, with the first element being the least significant byte of the given number, and the second element
     being the most significant byte.
    """
    if type(number) != int and type(number) != float:
        raise TypeError("number argument must always be a real number! {}".format(type(number)))

    raw_bytes_representation = float_to_raw_bytes(number, False)

    least_significant_byte = raw_bytes_to_int(raw_bytes_representation[2:4], low_bytes_first=False)
    most_significant_byte = raw_bytes_to_int(raw_bytes_representation[:2], low_bytes_first=False)

    return [least_significant_byte, most_significant_byte]


class FinsResponseBuilder(object):
    """
    Response builder which formats the responses as bytes.
    """

    def __init__(self):
        self.response = ""

    def add_int(self, value, length):
        """
        Adds an integer to the builder
        :param value: The integer to add
        :param length: How many bytes should the integer be represented as
        :return: The builder
        """
        self.response += int_to_raw_bytes(value, length, False)
        return self

    def add_float(self, value):
        """
        Adds an float to the builder (4 bytes, IEEE single-precision)
        :param value: The float to add
        :return: The builder
        """

        self.response += float_to_raw_bytes(value, False)
        return self

    def add_fins_frame_header(self, emulator_network_address, emulator_unit_address, client_network_address,
                              client_node, client_unit_address, service_id):
        """
        Makes a FINS frame header with the given data for a response to a client's command.

        The header bytes are as follows:
            1 byte (unsigned int): Information Control Field. It is always 0xC1 for a response.
            1 byte (unsigned int): Reserved byte. Always 0x00.
            1 byte (unsigned int): Gate count. Always 0x02 for our purposes.
            1 byte (unsigned int): Destination network address. For a response, it is the client's address.
            1 byte (unsigned int): Destination node address. For a response, it is the client's node.
            1 byte (unsigned int): Destination unit address. For a response, it is the client's unit.
            1 byte (unsigned int): Source network address. For a response, it is the emulator's address.
            1 byte (unsigned int): Source node address. For a response, it is the emulator's node.
            1 byte (unsigned int): Source unit address. For a response, it is the emulator's unit.
            1 byte (unsigned int): Service ID. It is a number showing what process generated the command sent by the
            client.

        :param emulator_network_address: The FINS network address of the emulator.
        :param emulator_unit_address: The FINS unit address of the emulator.
        :param client_network_address: The FINS network address of the client.
        :param client_node: The FINS node of the client.
        :param client_unit_address: The FINS unit address of the client.
        :param service_id: The service ID of the original command.
        :return: (ResponseBuilder) the builder with the fins frame header bytes.
        """

        return self.add_int(0xC1, 1).add_int(0x00, 1).add_int(0x02, 1) \
            .add_int(client_network_address, 1) \
            .add_int(client_node, 1) \
            .add_int(client_unit_address, 1) \
            .add_int(emulator_network_address, 1) \
            .add_int(SimulatedFinsPLC.HELIUM_RECOVERY_NODE, 1) \
            .add_int(emulator_unit_address, 1) \
            .add_int(service_id, 1)

    def add_fins_command_and_error_codes(self):
        """
        Adds the code for the FINS memory area read command and a default error code to the builder.
        :return: (ResponseBuilder) the builder with the command and error codes now added
        """

        # The memory area read command code is 0101, and the 0000 is the No error code.
        return self.add_int(0x0101, 2).add_int(0x0000, 2)

    def build(self):
        """
        Gets the response from the builder
        :return: the response
        """
        return self.response
