from gas import Gas

class SystemGases(object):
    def __init__(self):
        self.gases = dict()
        self.unmixable_pairs = set()
        self.buffer_gases = dict()

    def add_gas(self,gas):
        self.gases[gas.get_index()] = gas

    def get_gas_by_index(self,index):
        if index in self.gases.keys():
            return self.gases[index]
        else:
            return None

    def get_gas_by_name(self, name):
        try:
            return next(g for g in self.gases if g.get_name()==name)
        except StopIteration:
            return None

    def set_unmixable(self, gas1, gas2):
        self.set_unmixable(gas1.get_index(), gas2.get_index())

    def set_unmixable_by_name(self, name1, name2):
        self.set_unmixable(self.get_gas_by_name(name1), self.get_gas_by_name(name2))

    def set_unmixable_by_index(self, gas1_index, gas2_index):
        self.unmixable_pairs.add({gas1_index,gas2_index})

    def are_mixable(self, gas1, gas2):
        return self.are_mixable_by_index(gas1.get_index(), gas2.get_index())

    def are_mixable_by_index(self, gas1_index, gas2_index):
        return not {gas1_index,gas2_index} in self.unmixable_pairs

    def are_mixable_by_name(self, gas1_name, gas2_name):
        return self.are_mixable(self.get_gas_by_name(gas1_name), self.get_gas_by_name(gas2_name))

    def set_buffer_gas(self,key,gas_name):
        self.buffer_gases[key] = self.get_gas_by_name(gas_name)

    def add_gas(self,index,name):
        self.gases[index] = Gas(index,name)