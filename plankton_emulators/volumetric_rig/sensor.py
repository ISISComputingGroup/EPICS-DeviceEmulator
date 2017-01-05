from sensor_status import SensorStatus
from utilities import format_float


class Sensor(object):
    def __init__(self):
        self._status = SensorStatus.UNKNOWN
        self._value = 0.0

    def set_status(self, status):
        self._status = status

    def status(self):
        return self._status

    def set_value(self, v):
        self._value = v

    def value(self, as_string):
        return format_float(self._value, as_string)