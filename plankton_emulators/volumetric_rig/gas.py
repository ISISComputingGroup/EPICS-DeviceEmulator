from types import *


class Gas(object):
    def __init__(self,index,name):
        assert type(index) is IntType
        assert type(name) is StringType
        self.index = index
        self.name = name

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index

    def get_zero_padded_index(self,length=2):
        return str(self.index).zfill(length)

    def get_dash_padded_name(self,length):
        return self.get_padded_name(length,"-")

    def get_dot_padded_name(self,length):
        return self.get_padded_name(length,".")

    def get_padded_name(self,length,char):
        return self.name + char*(length-len(self.name))