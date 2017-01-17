class Mode(object):
    MODES = []


class AutoMode(Mode):
    AUTO = "AUTO"
    MANUAL = "MAN"
    MODES = [AUTO, MANUAL]


class ResistanceMode(AutoMode):
    pass


class ResistanceRangeMode(AutoMode):
    AUTO = "1"
    MANUAL = "0"
    MODES = [AUTO, MANUAL]


class SourceMode(Mode):
    CURRENT = "CURR"
    VOLTAGE = "VOLT"
    MODES = [CURRENT, VOLTAGE]


class OnOffMode(Mode):
    ON = "ON"
    OFF = "OFF"
    MODES = [ON, OFF]


class RemoteSensingMode(OnOffMode):
    pass


class OffsetCompensationMode(OnOffMode):
    pass


class OutputMode(OnOffMode):
    pass