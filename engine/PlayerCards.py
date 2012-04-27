import random
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
    os.path.pardir)))
from util.Functions import CardCounts
class PlayerCards(object):
    '''
        A deck is a tuple/list of a CardCounts of cards, number of cards. The discard, hand and 
        currentlyInPlay also share a similar structure
    '''
    def __init__(self, deck=CardCounts(), 
            discard=CardCounts(), hand=CardCounts(), currInPlay=CardCounts()):
        self.deck = deck
        self.discard = discard
        self.hand = hand
        self.currInPlay = currInPlay

    '''
        This method simulates the discard phase of the game.
    '''
    def discardPhase(self):
        self.discardcurrInPlay()
        self.discardHand()
        self.draw(5)
    '''
        This method puts the discard pile as the deck
    '''
    def discardToDeck(self):
        self.deck += self.discard
        self.discard = CardCounts()
    '''
        This method puts the deck into the discard pile
    '''
    def deckToDiscard(self):
        self.discard += self.deck
        self.deck = CardCounts()
 
    '''
        This method discards the currently in play cards into the 
        discard pile
    '''
    def discardcurrInPlay(self):
        self.discard += self.currInPlay
        self.currInPlay = CardCounts()
    '''
        This method discards the hand into the discard pile
    '''
    def discardHand(self):
        self.discard += self.hand
        self.hand = CardCounts()
    '''
        This method discards from hand several cards passed
        in as arguments.
    '''
    def discardFromHand(self,*args):
        for card in args:
            if (self.hand[card] > 0):
                self.discard[card] += 1
                self.hand[card] -= 1
    '''
        This method trashes from hand several cards passed in
        as arguments. Another class should keep track of trashed
        cards
    '''
    def trashFromHand(self, *args):
        for card in args:
            self.hand[card] -=1
    '''
        This method allows a player to reveal a card in the deck. This is
        implemented as a generator so that a player can keep revealing cards
        until a stop signal has been sent. Keep is a function which states
        which cards should be revealed and put in hand, and which cards should
        be discarded
    '''
    def revealCard(self, stop=False, keep=(lambda x : True)):
        tempCards = CardCounts()
        tempHand = CardCounts()
        while not stop:
            if not self.deck:
                if not self.discard:
                    break
                else:
                    self.discardToDeck()
            card = random.choice(self.deck.keys())
            if keep(card):
                tempHand[card] += 1
            else:
                tempCards[card] += 1
            yield card
        self.discard += tempCards
        self.hand += tempHand

    '''
        This method allows a person to gain a card
    '''
    def gain(self, card):
        self.discard[card] += 1
    '''
        This method draws N cards from the deck. If there are no more   
        cards during the drawing, the discard pile is shuffled and made
        into the deck. If there are also no more cards in the discard pile,
        then the drawing is done since there are no more cards to draw
    '''
    def draw(self, N):
        drawCards = []
        if self.deck:
            drawDeck = reduce(list.__add__, [[c]*self.deck[c] for c in self.deck])
            drawCards = random.sample(drawDeck, min(self.deck.count, N))
            N -= self.deck.count
        
        #In the case that there are no more cards to draw
        if (N > 0):
            if self.discard:
                discardDeck = reduce(list.__add__, 
                    [[c]*self.discard[c] for c in self.discard])
                drawCards += random.sample(discardDeck, min(self.discard.count, N))
                self.discardToDeck()
        
        for card in drawCards:
            self.hand[card] += 1
            self.deck[card] -= 1

