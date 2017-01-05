from sensor_status import SensorStatus


class Sensor(object):
    def __init__(self):
        self._status = SensorStatus.UNKNOWN

    def set_status(self, status):
        self._status = status

    def status(self):
        return self._status