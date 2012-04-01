import Card.py
'''
    Victory Card:
        +6 Victory Points
'''
@singleton
def Province(Card):
    def __init__(self):
        super(Province, name='Province', cost=8, 
                victoryPoints=6).__init__()
