from gas import Gas


class SystemGases(object):
    def __init__(self, gases=list()):
        self.gases = set()
        self._add_gases(gases)

    def gas_by_index(self, index):
        return self._get_by_method(index, "index")

    def gas_by_name(self, name):
        return self._get_by_method(name, "name")

    def _get_by_method(self, value, method):
        try:
            return next(g for g in self.gases if getattr(Gas, method) == value)
        except StopIteration:
            return None

    def _add_gases(self, iterable):
        self.gases += {g for g in iterable if isinstance(g, Gas)}
