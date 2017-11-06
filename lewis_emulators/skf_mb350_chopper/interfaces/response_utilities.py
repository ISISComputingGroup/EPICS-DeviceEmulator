from byte_conversions import int_to_raw_bytes, float_to_raw_bytes


def build_interlock_status(device):
    interlocks = device.get_interlocks()

    bit = 1
    result = 0
    for ilk in interlocks.values():
        result += bit if ilk else 0
        bit *= 2

    return result


def build_device_status(device):
    status_bits = [
        device.is_controller_ok(),
        device.is_up_to_speed(),
        device.is_able_to_run(),
        device.is_shutting_down(),
        device.is_levitation_complete(),
        device.is_phase_locked(),
        device.get_motor_direction() > 0,
        device.is_avc_on()
    ]

    bit = 1
    result = 0
    for stat in status_bits:
        result += bit if stat else 0
        bit *= 2
    return result


def phase_information_response_packet(address, device):
    return ResponseBuilder() \
        .add_int(address, 1) \
        .add_int(0xC0, 1) \
        .add_int(0x00, 1) \
        .add_int(build_device_status(device), 1) \
        .add_int(build_interlock_status(device), 2, low_byte_first=False) \
        .add_int(device.get_frequency(), 2) \
        .add_float(device.get_phase()) \
        .add_float(device.get_phase_repeatability()) \
        .add_float(device.get_phase_percent_ok()) \
        .build()


class ResponseBuilder(object):
    """
    Response builder which formats the responses as bytes.
    """

    def __init__(self):
        self.response = ""

    def add_int(self, value, length, low_byte_first=True):
        self.response += int_to_raw_bytes(value, length, low_byte_first)
        return self

    def add_float(self, value):
        self.response += float_to_raw_bytes(value)
        return self

    def build(self):
        return self.response