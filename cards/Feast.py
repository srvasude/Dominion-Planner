from Card import Card, singleton
'''
    Action Card:
        Trash this card. Gain a card costing up to 5 coins.
'''
@singleton
class Feast(Card):
    def __init__(self):
        super(Feast,self).__init__(name='Feast', cost=4, action=gainCard)

def gainCard(gameState):
    cardToChoose = InputClass.getSetInputs()
