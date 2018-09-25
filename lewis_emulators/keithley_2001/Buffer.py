from enum import Enum


class Buffer(object):

    def __init__(self):
        self._buffer = []
        self._size = 100
        self._source = Source.NONE
        self._mode = Mode.NEV
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

    @property
    def mode(self):
        return self._mode.name

    @mode.setter
    def mode(self, mode):
        try:
            self._mode = Mode[mode]
        except KeyError:
            raise ValueError("{} is not a valid buffer mode.".format(mode))

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if 2 <= size <= 404:
            self._size = size
        else:
            raise ValueError("{} is not a valid buffer size.".format(size))


class Source(Enum):
    NONE = 0
    SENS1 = 1
    CALC1 = 2


class Mode(Enum):
    NEV = 0
    NEXT = 1
    ALW = 2
    PRET = 3
