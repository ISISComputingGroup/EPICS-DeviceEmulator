from enum import Enum


class Channel(object):
    def __init__(self, channel):
        self.channel = channel
        self.reading = 0
        self.unit = Unit.VDC
        self.close = False


class StatusRegister(object):

    def __init__(self):
        self.buffer_full = False
        self.measurement_summary_status = False
        self.number_of_times_reset_and_cleared = 0

    def reset_and_clear(self):
        self.buffer_full = False
        self.measurement_summary_status = False
        self.number_of_times_reset_and_cleared += 1


class Unit(Enum):
    VDC = 0
    VAC = 1
    ADC = 2
    AAC = 3
    OHM = 4
    OHM4W = 5
    HZ = 6
    C = 7
    F = 8
    K = 9
