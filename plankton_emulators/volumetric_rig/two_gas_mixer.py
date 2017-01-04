class TwoGasMixer(object):
    def __init__(self):
        self.mixable = {}

    def add_mixable(self, gas1, gas2):
        self.mixable.add({gas1, gas2})

    def can_mix(self, gas1, gas2):
        return {gas1, gas2} in self.mixable
