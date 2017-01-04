class Valve(object):
    def __init__(self):
        self.is_enabled = True
        self.is_open = False

    def open(self):
        if self.is_enabled:
            self.is_open = True

    def close(self):
        if self.is_enabled:
            self.is_open = False