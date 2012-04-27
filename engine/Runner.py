import random
from ..cards
def play(cards, initialDeck, players):
    gs = GameState.setup(cards, intialDeck, players)
    numPlayers = len(gs.players);
    numDepleted = 0
    while (gs.stacks[Province()] != 0) and numDepleted < 3:
        curPlayer = gs.players[gs.turn]
        gs = curPlayer.playActionPhase(gs)
        gs = curPlayer.playBuyPhase(gs)
        gs = curPlayer.playDiscardPhase(gs)
        gs.turn = (gs.turn + 1) % numPlayers
        numDepleted = len(filter(lambda c: gs.stacks[c] == 0, cards))

players = []
chosenCards = random.sample(
<<<<<<< HEAD
    [Workshop(), Woodcutter(), Village(), Throne_room(), Smithy(), Remodel(), Moneylender(),
     Mine(), Market(), Laboratory(), Festival(), Feast(), Council_room(), Copper(), Chancellor()]
=======
    [Chancellor(), Chapel(), Council_room(),
     Feast(), Festival(), Laboratory(), Library(), Market(),
     Mine(), Moat(), Moneylender(), Remodel(), Smithy(), Throne_Room(), Village(), Woodcutter(), Workshop()]
>>>>>>> 9f76eb848ee26c8b12fdda85b160ec1869cc8db2
    , 10)
stacks = CardCounts(zip(chosenCards, [10] * len(chosenCards)))
stacks[Copper()] = 60 - 7 * len(players)
stacks[Silver()] = 40
stacks[Gold()] = 30
stacks[Estate()] = 24 - 3 * len(players)
stacks[Duchy()] = 12
stacks[Province()] = 12

play(stacks, CardCounts({Copper():7, Estate():3}), players)
