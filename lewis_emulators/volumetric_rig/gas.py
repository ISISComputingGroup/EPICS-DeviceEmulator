from types import StringType, IntType
from utilities import pad_string, format_int


class Gas(object):
    def __init__(self, index, name):
        assert type(index) is IntType and type(name) is StringType
        self._index = index
        self._name = name

    def name(self, length=None, padding_character=" "):
        return pad_string(self._name, length, padding_character)

    def index(self, as_string=False, length=2):
        return format_int(self._index, as_string, length)