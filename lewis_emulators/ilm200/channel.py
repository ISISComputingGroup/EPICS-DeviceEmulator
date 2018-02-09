class Channel(object):

    NITROGEN = 1
    HELIUM = 2
    HELIUM_CONT = 3
    CRYO_TYPES = (NITROGEN, HELIUM, HELIUM_CONT)

    FILL_RATE = 10.0

    def __init__(self, cryo_type):
        """
        Initialize all of the device's attributes.
        """
        self.level = 0.0
        self.fast_fill_rate = True
        assert cryo_type in Channel.CRYO_TYPES
        self.cryo_type = cryo_type

    def get_level(self):
        return self.level

    def is_fill_rate_fast(self):
        return self.fast_fill_rate

    def set_fill_rate(self, fast):
        self.fast_fill_rate = fast

    def get_cryo_type(self):
        return self.cryo_type
