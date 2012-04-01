from Card import Card, singleton
'''
    Victory Card:
        +6 Victory Points
'''
@singleton
class Province(Card):
    def __init__(self):
        super(Province, self).__init__(name='Province', cost=8, 
                victoryPoints=6)
