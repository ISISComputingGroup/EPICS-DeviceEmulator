from sensor_status import SensorStatus


class Sensor(object):
    def __init__(self):
        self.status = SensorStatus.UNKNOWN

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status