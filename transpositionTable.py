from collections import OrderedDict


class transTable:
    def __init__(self, size = 1000):
        self.table = OrderedDict()
    
    def set(self, key, value):
        if len(self.table) >= 1000:
            self.table.popitem(last = True)
        self.table[key] = value
    
    def lookup(self, key):
        if key in self.table:
            value = self.table[key]
            self.table.pop(key)
            self.table[key] = value
            return self.table[key]
        else:
            return None