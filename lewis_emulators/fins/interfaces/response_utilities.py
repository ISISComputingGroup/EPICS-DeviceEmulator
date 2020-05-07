from lewis_emulators.utils.byte_conversions import int_to_raw_bytes, float_to_raw_bytes
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


def dm_memory_area_read_response_fins_frame(device, client_network_address, client_node_address, client_unit_address,
                                            service_id, memory_start_address, number_of_words):

    # The length argument asks for number of bytes, and each word has two bytes
    return FinsResponseBuilder()\
        .add_fins_frame_header(device.network_address, device.unit_address, client_network_address,
                               client_node_address, client_unit_address, service_id) \
        .add_fins_command_and_error_codes() \
        .add_int(SimulatedFinsPLC.MEMORY_VALUE_MAPPING[memory_start_address], number_of_words * 2)\
        .build()


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
            .add_int(SimulatedFinsPLC.FINS_HE_RECOVERY_NODE, 1) \
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
