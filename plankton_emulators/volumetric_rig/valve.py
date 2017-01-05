from valve_status import ValveStatus


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

    def status(self):
        if self._is_open:
            return ValveStatus.OPEN_AND_ENABLED if self._is_enabled else ValveStatus.OPEN_AND_DISABLED
        else:
            return ValveStatus.CLOSED_AND_ENABLED if self._is_enabled else ValveStatus.CLOSED_AND_DISABLED

    def disable(self):
        self._is_enabled = False

    def enable(self):
        self._is_enabled = True
