import random
import sys 
import os.path 
from GameState import GameState
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 
    os.path.pardir)))
from cards import *
from util.Functions import CardCounts
from player.Simple_Player import Simple_Player
def play(cards, initialDeck, players):
    gs = GameState.setup(cards, initialDeck, players)
    numPlayers = len(gs.players);
    numDepleted = 0
    while (gs.stacks[Province.Province()] != 0) and numDepleted < 3:
        curPlayer = gs.players[gs.turn]
        gs = curPlayer.playActionPhase(gs)
        gs = curPlayer.playBuyPhase(gs)
        gs = curPlayer.playDiscardPhase(gs)
        gs.turn = (gs.turn + 1) % numPlayers
        numDepleted = len(filter(lambda c: gs.stacks[c] == 0, cards))
def main():
    players = [Simple_Player(), Simple_Player() ]
    chosenCards = random.sample(
        [Chancellor.Chancellor(), Council_room.Council_room(),
         Feast.Feast(), Festival.Festival(), Laboratory.Laboratory(), 
         Market.Market(), Mine.Mine(), Moneylender. Moneylender(), 
         Remodel.Remodel(), Smithy.Smithy(), Throne_room.Throne_room(), 
         Village.Village(), Woodcutter.Woodcutter(), Workshop.Workshop()]
        , 10)
    stacks = CardCounts(zip(chosenCards, [10] * len(chosenCards)))
    stacks[Copper.Copper()] = 60 - 7 * len(players)
    stacks[Silver.Silver()] = 40
    stacks[Gold.Gold()] = 30
    stacks[Estate.Estate()] = 24 - 3 * len(players)
    stacks[Duchy.Duchy()] = 12
    stacks[Province.Province()] = 12

    play(stacks, CardCounts({Copper.Copper():7, Estate.Estate():3}), players)

if __name__ == "__main__":
    main()
