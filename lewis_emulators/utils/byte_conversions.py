import struct

BYTE = 2**8


def int_to_raw_bytes(integer, length, low_byte_first):
    """
    Converts an integer to an unsigned set of bytes with the specified length (represented as a string).

    If low byte first is True, the least significant byte comes first, otherwise the most significant byte comes first.

    Args:
        integer (int): The integer to convert.
        length (int): The length of the result.
        low_byte_first (bool): Whether to put the least significant byte first.

    Returns:
        string:  string representation of the bytes.
    """
    result = r""

    for index in range(length):
        result += chr((integer // (BYTE**index)) % BYTE)

    return result if low_byte_first else result[::-1]


def raw_bytes_to_int(raw_bytes, low_bytes_first=True):
    """
    Converts an unsigned set of bytes to an integer.

    Args:
        raw_bytes (string): A string representation of the raw bytes.
        low_bytes_first (bool): Whether the given raw bytes are in little endian or not. True by default.

    Returns:
        int: The integer represented by the raw bytes passed in.
    """
    if not low_bytes_first:
        raw_bytes = raw_bytes[::-1]

    multiplier = 1
    result = 0
    for b in raw_bytes:
        result += ord(b) * multiplier
        multiplier *= BYTE
    return result


def float_to_raw_bytes(real_number, low_byte_first=True):
    """
    Converts an floating point number to an unsigned set of bytes.

    Args:
        real_number (int): The integer to convert.
        low_byte_first (bool): Whether to put the least significant byte first. True by default.

    Returns:
        string: A string representation of the bytes.
    """
    raw_bytes = "".join(chr(c) for c in bytearray(struct.pack(">f", real_number)))

    return raw_bytes[::-1] if low_byte_first else raw_bytes


def raw_bytes_to_float(raw_bytes):
    """
    Convert a set of bytes to a floating point number

    Args:
        raw_bytes (string): A stirng representation of the raw bytes.

    Returns:
        float: The floating point number represented by the given bytes.
    """
    return struct.unpack('f', raw_bytes[::-1])[0]
