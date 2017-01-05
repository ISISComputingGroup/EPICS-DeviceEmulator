from types import StringType


class EthernetDevice(object):
    def __init__(self, ip):
        assert type(ip) is StringType
        self._ip = ip

    def ip(self):
        return self._ip
