from Card import Card, singleton
'''
    Action Card:
        Choose any Action card in your hand. Play it twice.
'''
@singleton
class ThroneRoom(Card):
    def __init__(self):
        super(Card, self).__init__(name='ThroneRoom', cost=4, action=dbl)

def dbl(gameState):

