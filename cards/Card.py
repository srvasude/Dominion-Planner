class Card(object):
    def __init__(self, name='None', cost=0, coins=0, victoryPoints=0,
        action = None, reaction = None, ctype=None):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'cost', cost)
        object.__setattr__(self, 'coins', coins)
        object.__setattr__(self, 'victoryPoints', victoryPoints)
        object.__setattr__(self, 'action', action)
        object.__setattr__(self, 'reaction', reaction)
    def __hash__(self):
        return hash(getattr(self, 'name'))
    def __setattr__(*args):
        raise TypeError("Can't change immutable class")
    __delattr__ = __setattr__
    __slots__ = ('name', 'cost', 'coins', 'victoryPoints', 'action',
         'reaction')
     
def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance
