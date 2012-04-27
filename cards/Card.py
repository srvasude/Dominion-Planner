class Card(object):
    def __init__(self, name='None', cost=0, coins=0, victoryPoints=0,
            action = None, reaction = None, ctype=None):
        super(object, self).__setattr__('name', name)
        super(object, self).__setattr__('cost', cost)
        super(object, self).__setattr__('coins', coins)
        super(object, self).__setattr__('victoryPoints', victoryPoints)
        super(object, self).__setattr__('action', action)
        super(object, self).__setattr__('reaction', reaction)
     def __hash__(self):
         hsh = sum(hash(self.__getattr__(k)) for k in __slots__)
         return hsh
     def __setattr__(*args):
        raise TypeError("Can't change immutable class")
     __delattr__ = __setattr__
     __slots__ = ('name', 'cost', 'coins', 'victoryPoints', 'action',
             'reaction')
     
def singleton(cls):
    instances = {}
    def getinstance():
        if cls not instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance
