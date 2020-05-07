import struct

BYTE = 2**8


def int_to_raw_bytes(integer, length, low_byte_first):
    """
    Converts an integer to an unsigned set of bytes with the specified length (represented as a string).

    If low byte first is True, the least significant byte comes first, otherwise the most significant byte comes first.

    :param integer: (int) The integer to convert
    :param length: (int) The length of the result
    :param low_byte_first: (bool) Whether to put the least significant byte first
    :return (str) A string representation of the bytes.
    """
    result = r""

    for index in range(length):
        result += chr((integer // (BYTE**index)) % BYTE)

    return result if low_byte_first else result[::-1]


def raw_bytes_to_int(raw_bytes):
    """
    Converts an unsigned set of bytes to an integer.

    :param raw_bytes: (str) A string representation of the raw bytes.
    :return (int): The integer represented by the raw bytes passed in.
    """
    multiplier = 1
    result = 0
    for b in raw_bytes:
        result += ord(b) * multiplier
        multiplier *= BYTE
    return result


def float_to_raw_bytes(float_number, low_byte_first=True):
    """
    Converts an floating point number to an unsigned set of bytes.

    If low byte first is True, the least significant byte comes first, otherwise the most significant byte comes first.
    :param floatfloat_number: (int) The integer to convert.
    :param low_byte_first: (bool) Whether to put the least significant byte first. Treu by default.
    :return (str) A string representation of the bytes.
    """
    raw_bytes = "".join(chr(c) for c in bytearray(struct.pack(">f", float_number)))

    return raw_bytes[::-1] if low_byte_first else raw_bytes


def raw_bytes_to_float(raw_bytes):
    return struct.unpack('f', raw_bytes[::-1])[0]
