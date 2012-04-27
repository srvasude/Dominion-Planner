def play(cards, initialDeck, players):
    gs = GameState.setup(cards, intialDeck, players)
    numPlayers = len(gs.players);
    while (gs.stacks[Province()] != 0) && (< 3 Piles are depleted):
        curPlayer = gs.players[gs.turn]
        gs = curPlayer.playActionPhase(gs)
        gs = curPlayer.playBuyPhase(gs)
        gs = curPlayer.playDiscardPhase(gs)
        gs.turn = (gs.turn + 1) % numPlayers

players = []
chosenCards = random.sample(
    [Adventurer(), Bureaucrat(), Cellar(), Chancellor(), Chapel(), Council_room(),
     Feast(), Festival(), Gardens(), Laboratory(), Library(), Market(), Militia(),
     Mine(), Moat(), Moneylender(), Remodel(), Smithy(), Spy(), Thief(), Throne_room,
     Village(), Witch(), Woodcutter(), Workshop()]
    , 10)
stacks = CardCounts(zip(chosenCards, [10] * len(chosenCards)))
stacks[Copper()] = 60 - 7 * len(players)
stacks[Silver()] = 40
stacks[Gold()] = 30
stacks[Estate()] = 24 - 3 * len(players)
stacks[Duchy()] = 12
stacks[Province()] = 12

play(stacks, CardCounts({Copper():7, Estate():3}), players)
