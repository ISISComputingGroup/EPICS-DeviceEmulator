import unittest
from hamcrest import assert_that, is_, equal_to

from status_utils import convert_to_hexadecimal, DeviceStatus


class DeviceStatusTests(unittest.TestCase):
    """
    Tests that the device status is correctly converted.
    """

    def test_that_GIVEN_a_blank_device_status_THEN_all_hex_characters_zero(self):
        # Given:
        status = {
            "ON/OFF": False,
            "Fault condition": False,
            "Control mode": "Remote",
            "Regulation mode": False,
            "Update mode": "Normal",
            "Ramping": False,
            "Waveform": False,
            "OVT": False,
            "Mains fault": False,
            "Earth leakage": False,
            "Earth fuse": False,
            "Regulation fault": False,
            "Ext. interlock #1": False,
            "Ext. interlock #2": False,
            "Ext. interlock #3": False,
            "Ext. interlock #4": False,
            "DCCT fault": False,
            "OVP": False
        }
        device_status = DeviceStatus(status)

        # When:
        result = device_status.in_hexadecimal()

        # Then:
        expected = "0" * 8
        assert_that(result, is_(equal_to(expected)))

    def test_that_GIVEN_a_on_device_status_THEN_10000000_is_returned(self):
        # Given:
        status = {
            "ON/OFF": True,
            "Fault condition": False,
            "Control mode": "Remote",
            "Regulation mode": False,
            "Update mode": "Normal",
            "Ramping": False,
            "Waveform": False,
            "OVT": False,
            "Mains fault": False,
            "Earth leakage": False,
            "Earth fuse": False,
            "Regulation fault": False,
            "Ext. interlock #1": False,
            "Ext. interlock #2": False,
            "Ext. interlock #3": False,
            "Ext. interlock #4": False,
            "DCCT fault": False,
            "OVP": False
        }
        device_status = DeviceStatus(status)

        # When:
        result = device_status.in_hexadecimal()

        # Then:
        expected = "0" * 7 + "1"
        assert_that(result, is_(equal_to(expected)))

    def test_that_GIVEN_a_fault_condition_on_an_on_device_THEN_0000000_is_returned(self):
        # Given:
        status = {
            "ON/OFF": True,
            "Fault condition": True,
            "Control mode": "Remote",
            "Regulation mode": False,
            "Update mode": "Normal",
            "Ramping": False,
            "Waveform": False,
            "OVT": False,
            "Mains fault": False,
            "Earth leakage": False,
            "Earth fuse": False,
            "Regulation fault": False,
            "Ext. interlock #1": False,
            "Ext. interlock #2": False,
            "Ext. interlock #3": False,
            "Ext. interlock #4": False,
            "DCCT fault": False,
            "OVP": False
        }
        device_status = DeviceStatus(status)

        # When:
        result = device_status.in_hexadecimal()

        # Then:
        expected = "0" * 7 + "3"
        assert_that(result, is_(equal_to(expected)))


class ConvertBitsToHexTests(unittest.TestCase):
    """
    Tests for converting a word of 4 bits to the
    corresponding hexadecimal character.
    """

    def test_that_GIVEN_4_off_bits_THEN_zero_is_returned(self):
        # Given:
        word = [False, False, False, False]

        # When:
        result = convert_to_hexadecimal(word)

        # Then:
        expected = "0" * 8
        assert_that(result, is_(equal_to(expected)))

    def test_that_GIVEN_the_last_bit_on_THEN_one_is_returned(self):
        # Given:
        word = [False, False, False, True]

        # When:
        result = convert_to_hexadecimal(word)

        # Then:
        expected = "0" * 7 + "1"
        assert_that(result, is_(equal_to(expected)))

    def test_that_GIVEN_the_first_bit_on_THEN_eight_is_returned(self):
        # Given:
        word = [True, False, False, False]

        # When:
        result = convert_to_hexadecimal(word)

        # Then:
        expected = "0" * 7 + "8"
        assert_that(result, is_(equal_to(expected)))

    def test_that_GIVEN_32_bits_THEN_a_zero_padded_8_digit_hex_number_is_returned(self):
        # Given:
        bits = [False for _ in range(0, 32)]

        # When:
        result = convert_to_hexadecimal(bits)

        # Then:
        expected = "0" * 8
        assert_that(result, is_(equal_to(expected)))

    def test_that_GIVEN_32_bits_with_zeroth_one_on_THEN_00000001_is_returned(self):
        # Given:
        bits = [False for _ in range(0, 32)]
        bits[-1] = True

        # When:
        result = convert_to_hexadecimal(bits)

        # Then:
        expected = "0" * 7 + "1"
        assert_that(result, is_(equal_to(expected)))

    def test_that_GIVEN_32_bits_with_5th_bit_on_THEN_00000010_is_returned(self):
        # Given:
        bits = [False for _ in range(0, 32)]
        bits[-5] = True

        # When:
        result = convert_to_hexadecimal(bits)

        # Then:
        expected = "0" * 6 + "10"
        assert_that(result, is_(equal_to(expected)))
