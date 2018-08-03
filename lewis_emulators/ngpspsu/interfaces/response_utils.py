
# I want this to take in the status of the device
# and turn it into 8 hexadecimal integers
#
# 1. Each status key should be matched to a bit.
# 2. Work out each hexadecimal character
# 3. Join these up

REFERENCE = {
    "0": "ON/OFF",
    "1": "Fault condition",
    "2": "Control mode",
    "3": "Control mode",
    "5": "Regulation mode",
    "6": "Update mode",
    "7": "Update mode",
    "12": "Ramping",
    "13": "Waveform",
    "20": "OVT",
    "21": "Mains fault",
    "22": "Earth leakage",
    "23": "Earth fuse",
    "24": "Regulation fault",
    "26": "Ext. interlock #1",
    "27": "Ext. interlock #2",
    "28": "Ext. interlock #3",
    "29": "Ext. interlock #4",
    "30": "DCCT fault",
    "31": "OVP"
}


class DeviceStatus(object):

    def __init__(self, status):
        self._status = status

    def __str__(self):
        self._convert_status_to_bits(self._status)
        hexadecimals = self._get_hexadecimals()
        return "".join(hexadecimals)

    def _convert_status_to_bits(self, status):
        self.bits = [False for _ in range(0, 32)]

        for key, value in REFERENCE.items():
            self.bits[int(key)] = status[value]

    def _get_hexadecimals(self):
        return [str(Hexadecimal(self.bits[i, i+4])) for i in range(0, 31, 4)]


class Hexadecimal(object):
    """
    Hexadecimal character.

    Attributes:
        bits: list of booleans representing the bits of the hexadecimal char.
    """

    def __init__(self, bits):
        self.bits = bits

    def __str__(self):
        bits = self._parse_bits()
        return hex(int("".join(bits), 2))[-1]

    def _parse_bits(self):
        bits = []

        for bit in self.bits:
            bit_str = "1" if bit else "0"
            bits.append(bit_str)

        return bits


