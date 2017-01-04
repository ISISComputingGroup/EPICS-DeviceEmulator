from sensor import Sensor


class PressureSensor(Sensor):
    def __init__(self):
        self.pressure = 0.0
        super(PressureSensor,self).__init__()

    def set_pressure(self,pressure):
        self.pressure = pressure

    def get_pressure(self):
        return self.pressure