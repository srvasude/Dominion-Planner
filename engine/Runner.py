
def play(cards, initialDeck, players):
    gs = GameState.setup(cards, intialDeck, players)
    numPlayers = len(gs.players);
    while Provinces not Empty OR 3 Piles are not depleted:
        curPlayer = gs.players[gs.turn]
        gs = curPlayer.playActionPhase(gs)
        gs = curPlayer.playBuyPhase(gs)
        gs = curPlayer.playDiscardPhase(gs)
        gs.turn = (gs.turn + 1) % numPlayers
