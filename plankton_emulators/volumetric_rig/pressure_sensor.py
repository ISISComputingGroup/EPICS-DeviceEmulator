from sensor import Sensor
from sensor_status import SensorStatus
from random import random
from lewis.core.approaches import linear as linearApproach


class PressureSensor(Sensor):

    def __init__(self):
        super(PressureSensor, self).__init__()

    def set_value(self, v, target):
        super(PressureSensor, self).set_value(v)
        if self._value < 0.0:
            self._status = SensorStatus.VALUE_TOO_LOW
        elif self._value > target:
            self._status = SensorStatus.VALUE_TOO_HIGH
        else:
            self._status = SensorStatus.VALUE_IN_RANGE

    def approach_value(self, dt, target, rate):
        self._value = linearApproach(self._value, target, rate, dt)