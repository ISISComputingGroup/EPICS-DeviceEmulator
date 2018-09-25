from enum import Enum


class Channel(object):
    def __init__(self, channel):
        self.channel = channel
        self.reading = 0
        self.unit = ""


class ContScanningStatus(Enum):
    OFF = 0
    ON = 1
