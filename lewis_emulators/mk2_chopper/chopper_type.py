class ChopperType(object):
    """
    A type of chopper that the system can represent. Typically MK2 choppers come in 50Hz and 100Hz varieties.
    """

    # A dictionary of states the system can be in {Maximum frequency: [(Actual frequency, Max phase delay), ...]}
    VALID_SYSTEM_STATES = {
        50: [(5, 99995), (10,99995), (12.5, 79995), (16.67, 59995), (25, 39995), (50, 19995)],
        100: [(12.5, 79995), (25, 39995), (50, 19995), (100, 9995)]
    }

    def __init__(self, max_frequency):
        possible_max_frequencies = ChopperType.VALID_SYSTEM_STATES.keys()
        if max_frequency in possible_max_frequencies:
            self.max_frequency = max_frequency
        else:
            self.max_frequency = min(possible_max_frequencies)

    def get_closest_valid_frequency(self, frequency):
        return self._get_frequency_and_phase_closest_to_frequency(frequency)[0]

    def get_max_phase_for_closest_frequency(self, frequency):
        return self._get_frequency_and_phase_closest_to_frequency(frequency)[1]

    def _get_frequency_and_phase_closest_to_frequency(self, frequency):
        return min(ChopperType.VALID_SYSTEM_STATES[self.max_frequency], key=lambda x: abs(x - frequency))
