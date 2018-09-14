MEASUREMENT_TYPE = {0: "VOLT:DC", 1: "VOLT:AC", 2: "RES", 3: "FRES", 4: "CURR:DC", 5: "CURR:AC",
                    6: "FREQ", 7: "TEMP"}
BUFFER_SOURCE = {0: "SENS", 1: "CALC", 2: "NONE"}
BUFFER_CONTROL_MODE = {0: "NEXT", 1: "ALW", 2: "NEV"}
TIMESTAMP_FORMAT = {0: "ABS", 1: "DELT"}
CONTROL_SOURCE = {0: "IMM", 1: "TIM", 2: "MAN", 3: "BUS", 4: "EXT"}
SCAN_STATE = {0: "INT", 1: "NONE"}


class Channel(object):
    def __init__(self, channel):
        self.channel = channel
        self.reading = 0
        self.unit = ""
        self.timestamp = 0
