from types import StringType, IntType


class Gas(object):
    def __init__(self,index,name):
        assert type(index) is IntType and type(name) is StringType
        self.index = index
        self.name = name

    def name(self, length=None, padding_character=" "):
        return self.name if length is None \
            else self.name[:length] + (length-len(self.name))*padding_character

    def index_string(self, length=2):
        return str(self.index).zfill(length)