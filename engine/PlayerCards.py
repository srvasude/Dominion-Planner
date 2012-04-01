import random
class PlayerCards(Object):
    '''
        A deck is a tuple/list of a CardCounts of cards, number of cards
        and a CardCounts of visible cards. The discard, hand and 
        currentlyInPlay also share a similar structure without the 
        visible cards.
    '''
    def __init__(deck=None,discard=None,hand=None,currentlyInPlay=None):
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
        This method discards the currently in play cards into the 
        discard pile
    '''
    def discardcurrInPlay(self):
        self.discard[0] += self.currInPlay[0]
        self.discard[1] += self.currInPlay[1]
        self.currInPlay[0] = CardCounts()
        self.currInPlay[1] = 0
    '''
        This method discards the hand into the discard pile
    '''
    def discardHand(self):
        self.discard[0] += self.hand[0]
        self.discard[1] += self.hand[1]
        self.hand[0] = CardCounts()
        self.hand[1] = 0
    '''
        This method discards from hand several cards passed
        in as arguments.
    '''
    def discardFromHand(self,*args):
        for card in args:
            self.discard[0][card] += 1
            self.discard[1][card] += 1
            self.hand[0].decKey(card)
            self.hand[1] -= 1
    '''
        This method trashes from hand several cards passed in
        as arguments. Another class should keep track of trashed
        cards
    '''
    def trashFromHand(self, *args):
        for card in args:
            self.hand[0].decKey(card)
            self.hand[1] -= 1

    '''
        This method draws N cards from the deck. If there are no more   
        cards during the drawing, the discard pile is shuffled and made
        into the deck. If there are also no more cards in the discard pile,
        then the drawing is done since there are no more cards to draw
    '''
    def draw(self, N):
        for i in xrange(N):
            if not self.deck[0]:
                #In the case that there are no more cards to draw
                if not self.discard[0]:
                    return
                else:
                    self.deck[0] += self.discard[0]
                    self.deck[1] += self.discard[1]
                    self.discard[0] = CardCounts()
                    self.discard[1] = 0
            #Choose a random card from the deck
            card = random.choice(self.deck[0].keys())
            self.hand[0][card] += 1
            self.hand[1] += 1
            self.deck[0].decKey(card)
            self.deck[1] -= 1
