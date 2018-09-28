from enum import Enum


class Channel(object):
    def __init__(self, channel):
        self.channel = channel
        self.reading = 0
        self.unit = Unit.VDC
        self.close = False


class ContScanningStatus(Enum):
    OFF = 0
    ON = 1


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
