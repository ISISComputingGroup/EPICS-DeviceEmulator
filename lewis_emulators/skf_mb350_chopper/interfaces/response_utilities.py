from byte_conversions import int_to_raw_bytes, float_to_raw_bytes


def build_interlock_status(device):
    interlocks = device.get_interlocks()

    multiplier = 1
    result = 0

    for key in interlocks.keys():
        result += multiplier if interlocks[key] else 0
        multiplier *= 2

    return result


class Responses(object):
    """
    Utility class containing common responses (which may be shared between several commands).
    """
    @staticmethod
    def phase_information_response_packet(address, device):
        return ResponseBuilder()\
            .add_int(address, 1)\
            .add_int(0xC0, 1)\
            .add_int(0x00, 1)\
            .add_int(build_interlock_status(device), 2) \
            .add_int(device.get_frequency(address), 2) \
            .add_float(device.get_phase(address)) \
            .add_float(device.get_phase_repeatability(address)) \
            .add_float(device.get_phase_percent_ok(address)) \
            .build()


class ResponseBuilder(object):
    """
    Response builder which formats the responses as bytes.
    """

    def __init__(self):
        self.response = ""

    def add_int(self, value, length):
        self.response += int_to_raw_bytes(value, length)
        return self

    def add_float(self, value):
        self.response += float_to_raw_bytes(value)
        return self

    def build(self):
        return self.response