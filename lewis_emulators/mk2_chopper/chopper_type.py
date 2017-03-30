class ChopperType(object):

    FREQUENCY_TO_MAX_PHASE_CONVERSIONS = {5: 99995, 10: 99995, 12.5: 79995, 16.67: 59995,
                                          25: 39995, 50: 19995, 100: 9995}
    """
    A type of chopper that the system can represent. Typically MK2 choppers come in 50Hz and 100Hz varieties.

    Valid states are given as tuples with the first value being the frequency, the second value being the maximum
    phase delay.
    """
    def __init__(self, system_frequency, valid_frequencies):
        self.system_frequency = system_frequency
        self.valid_states = [(f, ChopperType.FREQUENCY_TO_MAX_PHASE_CONVERSIONS[f]) for f in valid_frequencies
                             if f in ChopperType.FREQUENCY_TO_MAX_PHASE_CONVERSIONS.keys()]
