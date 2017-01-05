from sensor import Sensor
from sensor_status import SensorStatus


class PressureSensor(Sensor):
    def __init__(self, target):
        self._target = target
        super(PressureSensor, self).__init__()

    def set_value(self, v):
        super(PressureSensor, self).set_value(v)
        if self._value < 0.0:
            self._status = SensorStatus.VALUE_TOO_LOW
        elif self._value > self._target:
            self._status = SensorStatus.VALUE_TOO_HIGH
        else:
            self._status = SensorStatus.VALUE_IN_RANGE