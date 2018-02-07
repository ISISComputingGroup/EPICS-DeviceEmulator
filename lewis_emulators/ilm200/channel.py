class Channel(object):

    FILL_RATE = 10.0

    def __init__(self):
        """
        Initialize all of the device's attributes.
        """
        self.level = 0.0
        self.fast_fill_rate = True

    def get_level(self):
        return self.level

    def is_fill_rate_fast(self):
        return self.fast_fill_rate

    def set_fill_rate(self, fast):
        self.fast_fill_rate = fast
