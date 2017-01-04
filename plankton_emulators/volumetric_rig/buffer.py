from valve import Valve


class Buffer(object):
    def __init__(self, index, buffer_gas, system_gas):
        self.buffer_gas = buffer_gas
        self.system_gas = system_gas
        self.index = index
        self.valve = Valve()

    def index_string(self, length=1):
        return str(self.index).zfill(length)
