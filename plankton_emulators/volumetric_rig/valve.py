class Valve(object):
    def __init__(self):
        self._is_enabled = True
        self._is_open = False

    def open(self):
        if self._is_enabled:
            self._is_open = True

    def close(self):
        if self._is_enabled:
            self._is_open = False

    def is_open(self):
        return self._is_open

    def is_enabled(self):
        return self._is_enabled