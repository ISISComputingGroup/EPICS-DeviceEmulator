from sensor import Sensor


class TemperatureSensor(Sensor):
    def __init__(self):
        self.temperature = 0.0
        super(TemperatureSensor,self).__init__()

    def set_temperature(self,temperature):
        self.temperature = temperature

    def get_temperature(self):
        return self.temperature