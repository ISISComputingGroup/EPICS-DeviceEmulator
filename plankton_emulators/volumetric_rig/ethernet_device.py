from types import StringType


class EthernetDevice(object):
    def __init__(self, ip):
        assert type(ip) is StringType
        self.ip = ip
