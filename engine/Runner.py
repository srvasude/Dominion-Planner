import random
import sys 
import os.path 
from GameState import GameState
from PlayerCards import PlayerCards
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 
    os.path.pardir)))
from cards import *
from util.Functions import CardCounts
from player.IHATEKARESH_Player import IHATEKARESH_Player
from player.Simple_Player import Simple_Player
from player.Human_Player import Human_Player

def play(cards, initialDeck, players):
    gs = GameState.setup(cards, initialDeck, players)
    numPlayers = len(gs.players);
    numDepleted = 0
    print "----------Game Starting--------------------"
    print numPlayers, 'players:', players
    print 'Starting deck:', str(initialDeck)
    print 'Stacks:', str(cards), '\n'
    gameLength = 0
    while (gs.stacks[Province.Province()] != 0) and numDepleted < 3:
        gameLength += 1
        curPlayer = gs.players[gs.turn]
        gs.abcs[gs.turn] = {'actions':1, 'buys':1, 'coins':0}
        import os
        os.system("clear")
        print("----------Player{0}'s turn--------------------".format(gs.turn))
        print 'Your deck:\t' + str(gs.pcards[gs.turn].deck)
        print 'Your discard:\t' + str(gs.pcards[gs.turn].discard)
        print 'Your hand:\t' + str(gs.pcards[gs.turn].hand)
        
        print("----------Player{0}'s action phase------------".format(gs.turn))
        gs = curPlayer.playActionPhase(gs)
        print("----------Player{0}'s buy phase ({1} coins, {2} buys)----"
                .format(gs.turn, gs.abcs[gs.turn]['coins'] + curPlayer.totalTreasure(gs), gs.abcs[gs.turn]['buys']))
        bought = gs.stacks.copy()
        gs = curPlayer.playBuyPhase(gs)
        print("----------Player{0}'s has bought: ({1})----".format(gs.turn, str(bought - gs.stacks)))
        gs = curPlayer.playDiscardPhase(gs)
        gs.turn = (gs.turn + 1) % numPlayers
        numDepleted = len(filter(lambda c: gs.stacks[c] == 0, cards))
        print("----------Player{0}'s turn has ended----------".format(gs.turn))
        print("----------------------------------------------\n")
    print "Game Over ({0} turns): ".format(gameLength)
    print 'remaining provinces: ', gs.stacks[Province.Province()]
    print 'depleted piles: ', numDepleted 
    
def main():
    chosenCards = random.sample(
        [Chancellor.Chancellor(), Council_room.Council_room(),
         Feast.Feast(), Festival.Festival(), Laboratory.Laboratory(), 
         Market.Market(), Mine.Mine(), Moneylender.Moneylender(), 
         Remodel.Remodel(), Smithy.Smithy(), Throne_room.Throne_room(), 
         Village.Village(), Woodcutter.Woodcutter(), Workshop.Workshop()]
        , 10)
    stacks = CardCounts(zip(chosenCards, [10] * len(chosenCards)))
    stacks[Copper.Copper()] = 60
    stacks[Silver.Silver()] = 40
    stacks[Gold.Gold()] = 30
    stacks[Estate.Estate()] = 24
    stacks[Duchy.Duchy()] = 12
    stacks[Province.Province()] = 12
    startDeck = CardCounts({Copper.Copper():7, Estate.Estate():3})
    
    NUMPLAYERS = 1
    stacks -= startDeck * NUMPLAYERS
    players = [IHATEKARESH_Player(stacks, startDeck)]
    #players = [Simple_Player()]
    play(stacks, startDeck, players)
    
if __name__ == "__main__":
    main()
