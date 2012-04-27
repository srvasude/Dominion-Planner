import sys 
import os.path 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 
    os.path.pardir)))
from util.Functions import CardCounts
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

