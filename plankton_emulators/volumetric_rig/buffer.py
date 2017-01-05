from valve import Valve
from utilities import optional_int_string_format
from two_gas_mixer import TwoGasMixer


class Buffer(object):
    def __init__(self, index, buffer_gas, system_gas):
        self._buffer_gas = buffer_gas
        self._system_gas = system_gas
        self._index = index
        self._valve = Valve()

    def index(self, as_string=False, length=1):
        return optional_int_string_format(self._index, as_string, length)

    def open_valve(self, mixer):
        assert isinstance(mixer, TwoGasMixer)
        if mixer.can_mix(self._buffer_gas, self._system_gas):
            self._valve.open()

    def close_valve(self):
        self._valve.close()

    def valve_is_open(self):
        return self._valve.is_open

    def valve_is_enabled(self):
        return self._valve.is_enabled
