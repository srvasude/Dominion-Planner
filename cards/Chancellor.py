from Card import Card, singleton
'''
    Action Card:
        +2 Coins
        You may immediately put your deck into your discard pile
'''
@singleton
class Chancellor(Card):
    def __init__():
        super(Card, self).__init__(name'Chancellor', cost=3, 
                action=gainDiscard)

def gainDiscard(gameState):
    gameState.abcs[gameState.turn]['coins'] += 2
    currentPlayer = gameState.players[gameState.turn]
    response = currentPlayer.selectInput(InputSets.tf(), 
            gameState)
    if response:
        gameState.pcards[gameState.turn].deckToDiscard()


