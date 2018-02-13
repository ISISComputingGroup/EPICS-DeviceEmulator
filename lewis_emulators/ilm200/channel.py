class Channel(object):

    NITROGEN = 1
    HELIUM = 2
    HELIUM_CONT = 3
    CRYO_TYPES = (NITROGEN, HELIUM, HELIUM_CONT)

    FAST_FILL_RATE = 50.0
    SLOW_FILL_RATE = 10.0
    GAS_USE_RATE = 5.0

    FULL = 95.0
    FILL = 5.0
    LOW = 10.0

    def __init__(self, cryo_type):
        """
        Initialize all of the device's attributes.
        """
        self.level = 0.0
        self.fast_fill_rate = True
        assert cryo_type in Channel.CRYO_TYPES
        self.cryo_type = cryo_type
        self.filling = False
        self.current = False

    def get_level(self):
        return self.level

    def is_fill_rate_fast(self):
        return self.fast_fill_rate

    def set_fill_rate(self, fast):
        self.fast_fill_rate = fast

    def get_cryo_type(self):
        return self.cryo_type

    def has_helium_current(self):
        return self.cryo_type in (Channel.HELIUM, Channel.HELIUM_CONT) and self.current

    def set_helium_current(self, is_on):
        self.current = self.cryo_type in (Channel.HELIUM, Channel.HELIUM_CONT) and is_on

    def trigger_auto_fill(self, cycle):
        if not cycle:  # Channel not cycling, use not filling level
            filling_trigger_level = Channel.FILL
        elif self.filling:  # Channel cycling but already filling. Only stop filling when full
            filling_trigger_level = Channel.FULL
        else:  # Channel cycling and not already filling. Start filling when it hits the filling level
            filling_trigger_level = Channel.FILL

        self.filling = self.level < filling_trigger_level

    def is_filling(self):
        return self.filling

    def start_filling(self):
        return self.level < Channel.FILL

    def is_level_low(self):
        return self.level < Channel.LOW