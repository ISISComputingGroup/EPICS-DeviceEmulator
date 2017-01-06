from valve import Valve
from utilities import format_int
from two_gas_mixer import TwoGasMixer


class Buffer(object):
    def __init__(self, index, buffer_gas, system_gas):
        assert buffer_gas is not None
        assert system_gas is not None
        self._buffer_gas = buffer_gas
        self._system_gas = system_gas
        self._index = index
        self._valve = Valve()

    def _disable_valve(self):
        self._valve.disable()

    def _enable_valve(self):
        self._valve.enable()

    def index(self, as_string=False, length=1):
        return format_int(self._index, as_string, length)

    def open_valve(self, mixer):
        assert isinstance(mixer, TwoGasMixer)
        if mixer.can_mix(self._buffer_gas, self._system_gas):
            self._valve.open()

    def close_valve(self):
        self._valve.close()

    def enable_valve(self):
        self._valve.enable()

    def disable_valve(self):
        # Valves must be closed before they are disabled
        self._valve.close()
        self._valve.disable()

    def valve_is_open(self):
        return self._valve.is_open()

    def valve_is_enabled(self):
        return self._valve.is_enabled()

    def valve_status(self):
        return self._valve.status()

    def buffer_gas(self):
        return self._buffer_gas

    def system_gas(self):
        return self._system_gas

    def set_system_gas(self, gas):
        if not self._valve.is_open():
            self._system_gas = gas