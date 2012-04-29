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
        self.cards = 0
        self.gamesPlayed = 0
    def incr(self, place):
        self.cards += place 
        self.gamesPlayed += 1
    def __cmp__(self, other):
        return cmp(self.cards/(1.0*self.gamesPlayed + 1),  
                other.cards/(1.0 * self.gamesPlayed + 1))
    def __repr__(self):
        string = ''
        for i in xrange(len(self.genes)):
            string += 'Gene {0}: {1} '.format(i, self.genes[i])
        return string
    def copy(self):
        c = Chromosome(*self.genes)
        c.cards = self.cards
        c.gamesPlayed = self.gamesPlayed
        return c
class GeneticAlgorithm(object):

    def __init__(self):
        #Parameters for Genetic Algorithm Tournament
        self.chromosomes = []
        self.generations = 0
        self.times_to_play = 10
        self.population_size = 40

        #Parameters for Crossing Genes
        self.mutate_by = 5
        self.mutation_rate = .2
        self.breeding_factor = .2
        self.crossover_rate = .3

        #Cards and Decks to test
        self.basic_cards = CardCounts({Copper.Copper() : 49, Silver.Silver() : 40, Gold.Gold() : 30, Estate.Estate() : 15, Duchy.Duchy() : 12, Province.Province() : 12})
        self.gameA = CardCounts({Market.Market() : 10, Village.Village() : 10, Woodcutter.Woodcutter() : 10, Smithy.Smithy() : 10, Laboratory.Laboratory() : 10, Festival.Festival() : 10, Council_room.Council_room() : 10, Mine.Mine() : 10, Feast.Feast() : 10, Chancellor.Chancellor() : 10}) + self.basic_cards
        self.goal_deckA = CardCounts({Gold.Gold() : 4, Silver.Silver() : 2, Village.Village() : 3, Market.Market() : 2, Festival.Festival() : 4, Laboratory.Laboratory() : 4, Woodcutter.Woodcutter() : 1})
        self.gameB = CardCounts({Throne_room.Throne_room() : 10, Remodel.Remodel() : 10, Mine.Mine() : 10, Workshop.Workshop() : 10, Feast.Feast() : 10, Festival.Festival() : 10, Market.Market() : 10, Smithy.Smithy() : 10, Moneylender.Moneylender() : 10, Chancellor.Chancellor() : 10}) + self.basic_cards
        self.goal_deckB = CardCounts({Gold.Gold() : 4, Throne_room.Throne_room() : 2, Smithy.Smithy() : 2, Festival.Festival() : 3, Mine.Mine() : 1, Market.Market() : 3})
        self.gameC = CardCounts() + self.basic_cards
        self.goal_deckC = CardCounts()
        self.games = [[self.gameA, self.goal_deckA], [self.gameB, self.goal_deckB], [self.gameC, self.goal_deckC]]

    #Initialize population
    def initialize(self):
        for i in xrange(self.population_size):
            state_gene = [random.randrange(-20,100) for j in xrange(5)]
            card_gene = [random.randrange(-20, 100) for j in xrange(3)]
            self.chromosomes.append(Chromosome(state_gene, card_gene))
    #When to finish GA
    def goal(self):
        return False

    #Check if any agent completed the goalDeck
    def suboptimalDeck(self, gameState, goalDeck):
        for cards in gameState.pcards:
            if not (goalDeck - cards.allCards()):
                return True
        return False

    #One step of the GA
    def step(self):
        print '=' * 50
        print 'Now Playing...'
        self.play()
        self.chromosomes.sort()
        print 'Generation {0} Best chromosome is {1}'.format(self.generations, self.chromosomes[0])
        print 'Crossing Over...'
        self.crossover()
        self.generations += 1

    #Crossover all the fit individuals
    def crossover(self): self._crossover1()

    #Crossover by
    def _crossover1(self):
        fit_indiv = self.chromosomes[:int(self.breeding_factor*self.population_size)]
        next_population = [self.chromosomes[0]]
        while len(next_population) < self.population_size:
            mate1 = random.choice(fit_indiv)
            if random.random() < self.crossover_rate:
                mate2 = random.choice(fit_indiv)
                first_pivot = random.randrange(0, len(mate1.genes[0]))
                second_pivot = random.randrange(0, len(mate1.genes[1]))
                child = [[], []]
                for i in xrange(first_pivot):
                    child[0].append(mate1.genes[0][i])
                child[0].extend(mate2.genes[0][first_pivot:])
                for i in xrange(second_pivot):
                    child[1].append(mate1.genes[1][i])
                child[1].extend(mate2.genes[1][second_pivot:])
                successor = Chromosome(*child) 
            else:
                successor = mate1.copy()
            self.mutate(successor)
            next_population.append(successor)
        self.chromosomes = next_population
    #Mutate chromosome
    def mutate(self, candidate):
        for gene in candidate.genes:
            for i in xrange(len(gene)):
                if random.random() < self.mutation_rate:
                    gene[i] += random.randrange(-self.mutate_by, self.mutate_by)
                    if gene[i] > 100:
                        gene[i] = 100
                    elif gene[i] < -20:
                        gene[i] = -20

    #Tournament to evaluate fittest individuals
    def play(self):
        sys.stdout.write('Iterating')
        startDeck = CardCounts({Copper.Copper():7, Estate.Estate():3})
        for chrm in self.chromosomes:
            sys.stdout.write('.')
            sys.stdout.flush()
            if chrm.gamesPlayed == self.times_to_play:
                continue
            who_to_play = filter((lambda x: x.gamesPlayed < self.times_to_play), self.chromosomes)
            tourn = random.sample(who_to_play, 2) 
            tourn.insert(0, chrm)
            gameType = random.choice(self.games)
            players = []
            for player in tourn:
                players.append(GUMDRP(gameType[1], *player.genes))
            gs = GameState.setup(gameType[0], startDeck, players)
            numPlayers = len(gs.players);
            numDepleted = 0
            numMoves = 0
            while (gs.stacks[Province.Province()] != 0) and numDepleted < 3 and not self.suboptimalDeck(gs, gameType[1]) and numMoves < 80:
                curPlayer = gs.players[gs.turn]
                gs.abcs[gs.turn] = {'actions':1, 'buys':1, 'coins':0}
                gs = curPlayer.playActionPhase(gs)
                bought = gs.stacks.copy()
                gs = curPlayer.playBuyPhase(gs)
                gs = curPlayer.playDiscardPhase(gs)
                gs.turn = (gs.turn + 1) % numPlayers
                numDepleted = len(filter(lambda c: gs.stacks[c] == 0, gs.stacks))
                numMoves += 1
            cards_left = [((gameType[1] - gs.pcards[i].allCards()).count, i) for i in xrange(numPlayers)]
            cards_left.sort()
            for people in cards_left:
                tourn[people[1]].incr(people[0])
        print ''

    #GA
    def run(self):
       self.initialize()
       while not self.goal():
            self.step()
def main():
    ga = GeneticAlgorithm()
    ga.run()
if __name__ == "__main__":
    main()
