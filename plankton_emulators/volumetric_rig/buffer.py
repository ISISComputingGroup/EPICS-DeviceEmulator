from valve import Valve
from utilities import optional_int_string_format


class Buffer(object):
    def __init__(self, index, buffer_gas, system_gas):
        self._buffer_gas = buffer_gas
        self._system_gas = system_gas
        self._index = index
        self._valve = Valve()

    def index(self, as_string=False, length=1):
        return optional_int_string_format(self._index, as_string, length)

    def valve(self):
        return self._valve