class DeviceStatus(object):
    """
    Converts the device's status to a list of 8 hexadecimal characters.
    """

    _REFERENCE = {
        "0": "ON/OFF",
        "1": "Fault condition",
        "2": "Control mode",
        "5": "Regulation mode",
        "6": "Update mode",
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

    _CONTROL_MODE = {
        "Remote": [False, False],
        "Local": [False, True]
    }

    _UPDATE_MODE = {
        "Normal": [False, False],
        "Waveform": [False, True],
        "Triggered FIFO": [True, False],
        "Analog Input": [True, True]
    }

    def __init__(self, status):
        self._status = status
        self._bits = [False for _ in range(0, 32)]

    def in_hexadecimal(self):
        """
        Returns the status of the device as a string of hexadecimal values.

        Returns:
            string: 8 hexadecimal values 0-F.
        """
        self._convert_status_to_bits(self._status)
        hexadecimals = self._get_hexadecimals()
        return "".join(hexadecimals)

    def _convert_status_to_bits(self, status):
        for key, value in self._REFERENCE.items():
            if value == "Control mode":
                self._bits[2:4] = self._CONTROL_MODE[status["Control mode"]]
            elif value == "Update mode":
                self._bits[6:8] = self._UPDATE_MODE[status["Update mode"]]
            else:
                self._bits[int(key)] = status[value]

    def _get_hexadecimals(self):
        bits = list(reversed(self._bits))

        return convert_to_hexadecimal(bits)


def convert_to_hexadecimal(word):
    """
    Converts  bits to a hexadecimal character.

    E.g.
        Converts [False, False, False, True] to "1".
        Converts [True, False, False, False] to "8"

    Args:
        word: List of 4 boolean values.

    Returns:
        string: Hexadecimal character 0-F corresponding to
            those 4 bits.
    """
    bits = []

    for bit in word:
        bit_str = "1" if bit else "0"
        bits.append(bit_str)

    int_bits_base_2 = int("".join(bits), 2)

    zero_padded_eight_digit_hexadecimal = "{0:#0{1}x}".format(int_bits_base_2, 10)

    # Removes 0x prefix
    zero_padded_eight_digit_hexadecimal = zero_padded_eight_digit_hexadecimal[2:]

    return zero_padded_eight_digit_hexadecimal
