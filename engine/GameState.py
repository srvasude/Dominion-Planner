import ../util/Functions.py
class GameState:
    @staticmethod
    def setup(cards, initialDeck, players):
        state = GameState()
        state.players = players
        state.pcards = [PlayerCards(deck = initialDeck) for p in players]
        for c in state.pcards:
            c.draw(5);
        state.abcs = [{'actions':0, 'buys':0, 'coins':0} for p in players]
        state.stacks = cards
        state.turn = 0
        state.trash = CardCounts()
        return state
    
    def clone(self):
        state = GameState()
        state.players = self.players
        state.pcards = self.pcards
        state.abcs = self.abcs
        state.stacks = self.stacks
        state.turn = self.turn
        state.trash = self.trash
        return state
    
    
