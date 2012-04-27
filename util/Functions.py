class CardCounts(dict):
    def __init__(self, *args, **kwargs):
        self.count = 0
        dict.__init__(self, *args, **kwargs)
        for key in self:
            self.count += self[key]
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)
    def __setitem__(self, key, value):
        if value <= 0:
            self.count -= self[key]
            del self[key]
        else:
            self.count -= (self[key] - value)
            dict.__setitem__(self, key, value)

    def sortedKeys(self):
        sortedItems = self.items()
        compare = lambda x, y:  sign(y[1] - x[1])
        sortedItems.sort(cmp=compare)
        return [x[0] for x in sortedItems]

    def totalCount(self):
        return self.count
    '''
    Return probabilities for each card
    '''
    def normalize(self):
        total = float(self.totalCount())
        if total == 0: return
        for key in self.keys():
            self[key] = self[key] / total
        self.count = 1

    def divideAll(self, divisor):
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor
        self.count /= divisor

    def copy(self):
        return CardCounts(dict.copy(self))

    def __mul__(self, y ):
        sum = 0
        x = self
        if len(x) > len(y):
            x,y = y,x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        for key, value in y.items():
            self[key] += value
            self.count += value

    def __add__( self, y ):
        addend = CardCounts()
        for key in self:
            if key in y:
                addend[key] = self[key] + y[key]
            else:
                addend[key] = self[key]
            addend.count += addend[key]
        for key in y:
            if key in self:
                continue
            addend[key] = y[key]
            addend.count += addend[key]
        return addend

    def decKey(self, key, num=1):
        curr = self[key]
        self[key] = curr - num if curr > num else 0
        self.count -= num if curr > num else 0
        if not self[key]:
            del self[key]

    def __sub__( self, y ):
        addend = CardCounts()
        for key in self:
            if key in y:
                addend[key] = self[key] - y[key]
            else:
                addend[key] = self[key]
            addend.count += addend[key]
        for key in y:
            if key in self:
                continue
            addend[key] = -1 * y[key]
            addend.count += addend[key]
        return addend


