class ErrorStates(object):
    def __init__(self):
        self.run = False
        self.hmi = False
        self.gauges = False
        self.comms = False
        self.estop = False