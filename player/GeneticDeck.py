import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 
    os.path.pardir)))
from cards import *
from GUMDRP import GUMDRP
from util.Functions import CardCounts
from engine.GameState import GameState
import scipy
from scipy import array
import random

def getDeck(cards, probs, size):
    deck = CardCounts(zip(cards, (int(round(p * size)) for p in probs)))
    return deck - deck * 0

def clean(probs, deckSize, locked=[0,1], maxNum = array([24, 60, 40, 30] + [10]*10)*.7):
    probs = probs / sum(probs)
    lockedProbs = probs[locked]
    probs *= deckSize
    probs = array([round(p) for p in probs])
    probs = array([min(p,m) for p,m in zip(probs, maxNum)])
    probs = probs / (sum(probs) - sum(probs[locked])) * (1 - sum(lockedProbs))
    probs[locked] = lockedProbs
    return probs

def mutate(probs, magnitude, locked = []):
    #probs = array([p + random.uniform(-magnitude, magnitude) for p in probs])
    probs = probs / sum(probs)
    lockedProbs = probs[locked]
    magnitude /= 3.0
    probs = array([bool(p) * max(0, p + scipy.random.normal(0, magnitude)) for p in probs])
    probs = probs / (sum(probs) - sum(probs[locked])) * (1 - sum(lockedProbs))
    probs[locked] = lockedProbs
    return probs

def evalDeck(player, deck, trials = 5):
    totalBuyingPower = 0
    totalAquiredValue = 0
    #state = GameState.setup(deck.copy(), deck.copy(), [player])
    for t in xrange(trials):
        state = GameState.setup(deck.copy(), deck.copy(), [player])
        state.abcs[0] = {'actions':1, 'buys':1, 'coins':0}
        #print str(state.pcards[0].hand)
        aquired = state.stacks.copy()
        state = state.players[0].playActionPhase(state)
        aquired -= state.stacks
        totalAquiredValue += sum([c.cost*n for c,n in aquired.items()])
        totalCoins = state.abcs[0]['coins'] + sum([c.coins*n for c,n in state.pcards[0].hand.items()])
        totalBuyingPower += min(state.abcs[0]['buys']*8, totalCoins)
        state = state.players[0].playDiscardPhase(state)
        #print totalBuyingPower, '~\tbuys:', state.abcs[0]['buys'], '\tcoins:', totalCoins, '\taquired:', str(aquired), '\n'
    return (totalBuyingPower, totalAquiredValue)

def generateDeck(cards, initProbs, locked, deckSize, player, trials = [(10,10),(10,3),(10,1)]):
    for (tr,mag) in trials:
        dv = range(tr)
        for t in xrange(tr):
            probs = clean(initProbs, deckSize)
            probs = clean(mutate(probs, 3.*mag/deckSize, locked=locked), deckSize)
            dv[t] = (evalDeck(player, getDeck(cards, probs, deckSize)), t, probs)
        initProbs = max(dv)[2]
    return getDeck(cards, initProbs, deckSize)
    
def main():
    cards = [Chancellor.Chancellor(), Council_room.Council_room(),
             Feast.Feast(), Festival.Festival(), Laboratory.Laboratory(), 
             Market.Market(), Mine.Mine(), Moneylender.Moneylender(), 
             Remodel.Remodel(), Smithy.Smithy(), Throne_room.Throne_room(), 
             Village.Village(), Woodcutter.Woodcutter(), Workshop.Workshop()]
    cards = [Estate.Estate(), Copper.Copper(), Silver.Silver(), Gold.Gold()] + random.sample(cards, 10) 
    deckSize = 25
    psc = 2.0*7/deckSize #percent starting coppers
    pse = 2.0*3/deckSize #percent starting estates
    initProbs = array([pse, psc, .5*(1-psc-pse), .5*(1-psc-pse)]+[1.0/10]*10)
    initProbs = initProbs / sum(initProbs)
    player = GUMDRP(getDeck(cards, initProbs, deckSize), (0,5,5,0,1), (0,0,0,0,0,0,0,0))
    
    print generateDeck(cards, initProbs, range(2), deckSize, player, trials = [(15,10),(10,3),(10,1)])
    
    '''
    trials = 10
    dv = range(trials)
    for t in xrange(trials):
        probs = clean(mutate(initProbs, 1, locked=range(2)), deckSize)############################################
        deck = getDeck(cards, probs, deckSize)
        dv[t] = (evalDeck(player, deck), t, probs)
        print dv[t][0], '\t', deck
    best = max(dv)
    print best
    print str(getDeck(cards, best[2], deckSize))
    print

    trials = 10
    dv = range(trials)
    for t in xrange(trials):
        probs = clean(mutate(best[2], 3.*3/deckSize, locked=range(2)), deckSize)
        deck = getDeck(cards, probs, deckSize)
        dv[t] = (evalDeck(player, deck), t, probs)
        print dv[t][0], '\t', deck
    best = max(dv)
    print best
    print str(getDeck(cards, best[2], deckSize))
    
    trials = 10
    dv = range(trials)
    for t in xrange(trials):
        probs = clean(mutate(best[2], 3.*1/deckSize, locked=range(2)), deckSize)
        deck = getDeck(cards, probs, deckSize)
        dv[t] = (evalDeck(player, deck), t, probs)
        print dv[t][0], '\t', deck
    best = max(dv)
    print best
    print str(getDeck(cards, best[2], deckSize))
    '''

if __name__ == "__main__":
    main()
