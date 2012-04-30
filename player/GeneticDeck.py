import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 
    os.path.pardir)))
from cards import *
from GeneticDeckHelper import GeneticDeckHelper
from util.Functions import CardCounts
from engine.GameState import GameState
import scipy
from scipy import array, append, nan
import itertools
import random

def getDeck(cards, probs, size):
    nums = array([int(round(p)) for p in probs*size])
    deck = CardCounts(zip(cards, nums))
    return deck - deck * 0

def clean(probs, deckSize, locked=[0,1], maxNum = array([24, 60, 40, 30] + [10]*10)*.7):
    if sum(probs)-sum(probs[locked]) == 0:
        return probs/sum(probs) if sum(probs) else array(probs)
    probs = probs / sum(probs)
    lockedProbs = probs[locked]
    probs *= deckSize
    probs = array([round(p) for p in probs])
    maxed = []
    maxedProbs = array([])
    for i in xrange(len(probs)):
        if probs[i] > maxNum[i] and i not in locked:
            maxed += [i]
            maxedProbs = append(maxedProbs, 1.*maxNum[i]/deckSize)
    if (sum(probs) - sum(probs[locked]) - sum(probs[maxed])) == 0:
        probs[locked] = lockedProbs
        probs[maxed] = maxedProbs
        return probs
    probs = probs / (sum(probs) - sum(probs[locked]) - sum(probs[maxed])) * (1 - sum(lockedProbs) - sum(maxedProbs))
    probs[locked] = lockedProbs
    probs[maxed] = maxedProbs
    if array([round(probs[i]*deckSize)>maxNum[i] for i in xrange(len(probs)) if i not in locked]).any():
        return clean(probs, deckSize, locked = locked + maxed)
    return probs

def mutate(probs, magnitude, locked = []):
    #probs = array([p + random.uniform(-magnitude, magnitude) for p in probs])
    probs = probs / sum(probs)
    lockedProbs = probs[locked]
    magnitude /= 3.0
    probs = array([bool(p) * max(0, p + scipy.random.normal(0, magnitude)) for p in probs])
    if sum(probs)-sum(probs[locked]) == 0:
        probs[locked] = lockedProbs
        return array(probs)
    probs = probs / (sum(probs) - sum(probs[locked])) * (1 - sum(lockedProbs))
    probs[locked] = lockedProbs
    return probs

def evalDeck(player, stacks, deck, trials = 5, coinsPerBuy=8, aquireFilter = lambda c:True):
    totalBuyingPower = 0
    totalAquiredValue = 0
    state = GameState.setup(stacks.copy(), deck.copy(), [player])
    #print str(deck)
    for t in xrange(trials):
        #state = GameState.setup(deck.copy(), deck.copy(), [player])
        state.abcs[0] = {'actions':1, 'buys':1, 'coins':0}
        #print str(state.pcards[0].hand)
        aquired = state.stacks.copy()
        state = state.players[0].playActionPhase(state)
        aquired -= state.stacks
        totalAquiredValue += sum([c.cost*n for c,n in aquired.items() if aquireFilter(c)])
        totalCoins = state.abcs[0]['coins'] + sum([c.coins*n for c,n in state.pcards[0].hand.items()])
        totalBuyingPower += min(state.abcs[0]['buys']*coinsPerBuy, totalCoins)
        state = state.players[0].playDiscardPhase(state)
        #print totalBuyingPower, '~\tbuys:', state.abcs[0]['buys'], '\tcoins:', totalCoins, '\taquired:', str(aquired), '\n'
    return (totalBuyingPower, totalAquiredValue)

def generateDeck(stacks, cards, initProbs, locked, deckSize, params = (0,5,1,0,3),
                coinsPerBuy=8, prioritizeAquires=False, aquireFilter = lambda c:True,
                trials = [(10,10),(10,3),(10,1)], maxNum = array([24, 60, 40, 30] + [10]*10)*.7):
    for (tr,mag) in trials:
        dv = range(tr)
        for t in xrange(tr):
            probs = array(initProbs)
            probs = clean(mutate(probs, 3.*mag/deckSize, locked=locked), deckSize, maxNum=maxNum)
            deck = getDeck(cards, probs, deckSize)
            player = GeneticDeckHelper(params)
            if prioritizeAquires:
                dv[t] = (sum(evalDeck(player, stacks, deck, aquireFilter=aquireFilter)), t, probs)
            else:
                dv[t] = (evalDeck(player, stacks, deck), t, probs)
        initProbs = max(dv)[2]
    return getDeck(cards, initProbs, deckSize)

def generateMiniDeck(stacks, cards, params, deckSize=13, reps = 2, turns=5):
    best = (-1, -1, None)
    t=0
    initCards = itertools.combinations_with_replacement(
        [c for c in cards if c.cost<5 and c!=Copper.Copper() and c!=Estate.Estate()], deckSize-10)
    for cs in initCards:
        deck = CardCounts({Copper.Copper():7, Estate.Estate():3})
        for c in cs:
            deck[c] += 1
        player = GeneticDeckHelper(params)
        aquireFilter = lambda c: c.cost>=5
        deckVal = sum([sum(evalDeck(player, stacks, deck, trials=turns, coinsPerBuy=6, aquireFilter=aquireFilter)) for i in xrange(reps)])
        best = max(best, (deckVal, t, deck))
        t += 1
    return best[2]
    '''
    miniDeckSize = 13
    miniCards = [c for c in cards if c.cost<5]    
    psc = 7./miniDeckSize #percent starting coppers
    pse = 3./miniDeckSize #percent starting estates
    miniInitProbs = array([pse, psc] + [(1.0-psc-pse)/(len(miniCards)-2)]*(len(miniCards)-2))
    print generateDeck(miniCards, miniInitProbs, range(2), miniDeckSize, params=params,
        coinsPerBuy=6, prioritizeAquires=True, trials = [(225,miniDeckSize/3.),(15,3),(10,1)], maxNum = array([24, 60, 40]+[10]*10)*.7)
    '''

def generateGoalDeck(stacks, cards, params, reps = 2, deckSize=17, stages = [(15,17/3.),(10,3),(10,1)]):
    psc = 7./deckSize #percent starting coppers
    pse = 3./deckSize #percent starting estates
    cards = [c for c in cards if c.action]
    cards = [Estate.Estate(), Copper.Copper(), Silver.Silver(), Gold.Gold()] + cards
    #initProbs = array([pse, psc, .5*(1-psc-pse), .5*(1-psc-pse)]+[1.0/10]*10)
    initProbs = array([pse, psc]+[(1.0-pse-psc)/(len(cards)-2)]*(len(cards)-2))
    initProbs = initProbs / sum(initProbs)
    bestDecks = [generateDeck(stacks, cards, initProbs, range(2), deckSize, params = params,
        coinsPerBuy=8, prioritizeAquires=True, aquireFilter = lambda c: c==Province.Province(),
        trials = stages) for bd in xrange(reps)]
    bestDecks = [(evalDeck(GeneticDeckHelper(params), stacks, bestDecks[bd]), bd, bestDecks[bd]) for bd in xrange(reps)]
    return max(bestDecks)[2]
    
def main():
    cards = [Chancellor.Chancellor(), Council_room.Council_room(),
             Feast.Feast(), Festival.Festival(), Laboratory.Laboratory(), 
             Market.Market(), Mine.Mine(), Moneylender.Moneylender(), 
             Remodel.Remodel(), Smithy.Smithy(), Throne_room.Throne_room(), 
             Village.Village(), Woodcutter.Woodcutter(), Workshop.Workshop()]
    cards = [Estate.Estate(), Copper.Copper(), Silver.Silver(), Gold.Gold()] + random.sample(cards, 10) 
    stacks = CardCounts(zip(cards,[20]*len(cards)))
    stacks[Province.Province()] = 20
    
    params = (0,5,1,0,3) #[35, -2, -10, -17, 45], [27,-19,-3,-5,100], [73, 28, -3, 42, -20]
    
    
    print [c.name for c in cards[4:]]
    goalD = generateGoalDeck(stacks, cards, params, reps = 1, deckSize = 17)
    print sum([evalDeck(GeneticDeckHelper(params), stacks, goalD)[0] for xx in xrange(5)])/5., goalD
    miniD = generateMiniDeck(stacks, cards, params, reps = 1)
    print sum([sum(evalDeck(GeneticDeckHelper(params),stacks, miniD)) for xx in xrange(5)])/5., miniD


    

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
