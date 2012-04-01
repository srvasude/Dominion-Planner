import card.py
@singleton
def Laboratory(Card):
    def __init__(self):
        super(Card, name="Laboratory", coins = 0, victoryPoints=0, 
                action = act, reaction = None).__init__()
'''
    Action Card:
        +2 Cards
        +1 Action
'''
def act(gameState):

