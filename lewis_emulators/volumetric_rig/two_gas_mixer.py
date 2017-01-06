class TwoGasMixer(object):
    def __init__(self):
        self.mixable = set()

    def add_mixable(self, gas1, gas2):
        self.mixable.add(frozenset([gas1, gas2]))

    def can_mix(self, gas1, gas2):
        return frozenset([gas1, gas2]) in self.mixable
