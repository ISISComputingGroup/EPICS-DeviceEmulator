from valve import Valve
from utilities import format_int
from two_gas_mixer import TwoGasMixer


class Buffer(object):

    PRESSURE_RATE = 1.0

    def __init__(self, index, buffer_gas, system_gas):
        assert buffer_gas is not None
        assert system_gas is not None
        self._buffer_gas = buffer_gas
        self._system_gas = system_gas
        self._index = index
        self._valve = Valve()
        self._pressure = 0.0

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

    def update_pressure(self, dt, pressure_limit):
        if self._valve.is_open():
            self._pressure += Buffer.PRESSURE_RATE*dt
        else:
            self._pressure -= Buffer.PRESSURE_RATE*dt

        if self._pressure > pressure_limit:
            self.close_valve()
            self._disable_valve()

    def pressure(self):
        return self._pressure