


P = First Player
Everyone draws 5 at the beginning
While Provinces not Empty OR 3 Piles are not depleted
    P Action Phase
    P Buy Phase
    P Discard Hand, Redraw 5*
    P = Next Player
End While


def play(cards, initialDeck, players):
    gs = GameState.setup(cards, intialDeck, players)
    numPlayers = len(gs.players);
    while ():
        gs = gs.players[turn % numPlayers].playActionPhase(gs)
        gs = gs.players[turn % numPlayers].playBuyPhase(gs)
        gs.pcards[turn % numPlayers].discardPhase()
        gs.turn += 1
        
        
