import random
from GUMDRP import GUMDRP
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 
    os.path.pardir)))
from cards import *
from util.Functions import CardCounts
from engine.GameState import GameState
class Chromosome(object):
    def __init__(self, *genes):
        self.genes = genes
        self.wins = 0
        self.second = 0
        self.gamesPlayed = 0
    def incr(self, place):
        if place == 0:
            self.wins += 1
        elif place == 1:
            self.second += 1
        self.gamesPlayed += 1
    def __cmp__(self, other):
        return cmp((self.wins/(1.0 * self.gamesPlayed + 1), self.second), 
                (other.wins/(1.0 * self.gamesPlayed + 1), other.second))
    def __repr__(self):
        string = ''
        for i in xrange(len(genes)):
            string += 'Gene {0}: {1} '.format(i, genes[i])
        print string
    def copy(self):
        c = Chromosome(self.genes)
        c.wins = self.wins
        c.second = self.second
        c.gamesPlayed = self.gamesPlayed
        return c
#Parameters for Genetic Algorithm Tournament
chromosomes = []
generations = 0
times_to_play = 18
population_size = 100

#Parameters for Crossing Genes
mutate_by = 5
mutation_rate = .2
breeding_factor = .2
crossover_rate = .5

#Cards and Decks to test
basic_cards = CardCounts({Copper.Copper() : 60, Silver.Silver() : 40, Gold.Gold() : 30, Estate.Estate() : 24, Duchy.Duchy() : 12, Province.Province() : 12})
gameA = CardCounts() + basic_cards
goal_deckA = CardCounts()
gameB = CardCounts() + basic_cards
goal_deckB = CardCounts()
gameC = CardCounts() + basic_cards
goal_deckC = CardCounts()
games = [[gameA, goal_deckA], [gameB, goal_deckB], [gameC, goal_deckC]]

#Initialize population
def initialize():
    for i in xrange(population_size):
        state_gene = [random.randrange(-100,100) for j in xrange(5)]
        card_gene = [random.randrange(-100, 100) for j in xrange(3)]
        chromosomes.append(Chromosome(state_gene, card_gene))
#When to finish GA
def goal():
    return generations > 6

#Check if any agent completed the goalDeck
def suboptimalDeck(gameState, goalDeck):
    for cards in gameState.pcards:
        if not (goalDeck - cards.allCards()):
            return True
    return False

#One step of the GA
def step():
    print '=' * 50
    print 'Now Playing...'
    play()
    chromosomes.sort()
    print 'Generation {0} Best chromosome is {1}'.format(generations, chromosomes[0])
    print 'Crossing Over...'
    crossover()
    generations += 1

#Crossover all the fit individuals
def crossover(): _crossover1()

#Crossover by
def _crossover1():
    fit_indiv = chromosomes[:int(breeding_factor*population_size)]
    next_population = [chromosomes[0]]
    while len(next_population) < population_size:
        mate1 = random.choice(fit_indiv)
        if random.random() < crossover_rate:
            mate2 = random.choice(fit_indiv)
            first_pivot = random.randrange(0, len(mate1[0]))
            second_pivot = random.randrange(0, len(mate1[1]))
            child = [[], []]
            for i in xrange(first_pivot):
                child[0].append(mate1[0][i])
            child[0].extend(mate2[0][first_pivot:])
            for i in xrange(second_pivot):
                child[1].append(mate1[1][i])
            child[1].extend(mate2[1][second_pivot:])
        else:
            child = mate1.copy()
        mutate(child)
        next_population.append(individual)
    chromosomes = next_population
    
def _crossover2(): pass
def _crossover3(): pass

def mutate(chromosome):
    for gene in chromosome:
        for i in len(gene):
            if random.random() < mutation_rate:
                gene[i] += random.randrange(-mutate_by, mutate_by)

#Tournament to evaluate fittest individuals
def play():
    startDeck = CardCounts({Copper.Copper():7, Estate.Estate():3})
    for chrm in chromosomes:
        if chrm.gamesPlayed == times_to_play:
            continue
        who_to_play = filter((lambda x: x.gamesPlayed < 10), chromosomes)
        tourn = random.sample(chromosomes, 2) 
        tourn.insert(0, chrm)
        gameType = random.choice(games)
        players = []
        for player in tourn:
            players.append(GUMDRP(gameType[1], *player.genes))
        gs = GameState.setup(gameType[0], startDeck, players)
        numPlayers = len(gs.players);
        numDepleted = 0
    while (gs.stacks[Province.Province()] != 0) and numDepleted < 3 and not suboptimalDeck(gs, gameType[1]):
        curPlayer = gs.players[gs.turn]
        gs.abcs[gs.turn] = {'actions':1, 'buys':1, 'coins':0}
        gs = curPlayer.playActionPhase(gs)
        bought = gs.stacks.copy()
        gs = curPlayer.playBuyPhase(gs)
        gs = curPlayer.playDiscardPhase(gs)
        gs.turn = (gs.turn + 1) % numPlayers
        numDepleted = len(filter(lambda c: gs.stacks[c] == 0, cards))
    cards_left = [((gameType[1] - gs.pcards[i].allCards()).count, i) 
        for i in xrange(numPlayers)]
    cards_left.sort()
    for people in cards_left:
        tourn[people[1]].incr(people[1])

#GA
def main():
    initialize()
    while not goal():
        step()
if __name__ == "__main__":
    main()
