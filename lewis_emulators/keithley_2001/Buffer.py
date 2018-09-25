from enum import Enum


class Buffer(object):

    def __init__(self):
        self._buffer = []
        self._source = Source.NONE
        self.number_of_times_buffer_cleared = 0

    def clear_buffer(self):
        self._buffer = []
        self.number_of_times_buffer_cleared += 1

    @property
    def source(self):
        return self._source.name

    @source.setter
    def source(self, source):
        try:
            self._source = Source[source]
        except KeyError:
            raise ValueError("{} is not a valid buffer source.".format(source))


class Source(Enum):
    NONE = 0
    SENS1 = 1
    CALC1 = 2
