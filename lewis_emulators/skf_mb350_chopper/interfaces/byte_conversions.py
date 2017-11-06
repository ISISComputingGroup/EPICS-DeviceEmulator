import struct

BYTE = 2**8


def int_to_raw_bytes(integer, length, low_byte_first):
    """
    Converts an integer to an unsigned set of bytes with the specified length (represented as a string).

    If low byte first is True, the least significant byte comes first, otherwise the most significant byte comes first.
    """
    result = r""

    for index in range(length):
        result += chr((integer // (BYTE**index)) % BYTE)

    return result if low_byte_first else result[::-1]


def raw_bytes_to_int(raw_bytes):
    """
    Converts an unsigned set of bytes to an integer.
    """
    multiplier = 1
    result = 0
    for b in raw_bytes:
        result += ord(b) * multiplier
        multiplier *= BYTE
    return result


def float_to_raw_bytes(fl):
    return "".join(chr(c) for c in bytearray(struct.pack(">f", fl)))


def raw_bytes_to_float(raw_bytes):
    return struct.unpack('f', raw_bytes)[0]
