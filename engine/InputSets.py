import itertools

class InputSets:
    def tf():
        @staticmethod
        return set(True, False)
    
    def handCardSet(gameState):
        @staticmethod
        hand = gameState.pcards[gameState.turn].hand;
        handCards = itertools.chain.from_iterable
                        ((itertools.repeat(c, hand.cards[c]) for c in hand.cards))
        return itertools.chain.from_iterable
                        ([itertools.combinations(handCards, i) for i in range(hand.size + 1)])
    
    def nHandCardSet(gameState, n):
        @staticmethod
        hand = gameState.pcards[gameState.turn].hand;
        handCards = itertools.chain.from_iterable
                        ((itertools.repeat(c, hand.cards[c]) for c in hand.cards))
        return itertools.combinations(handCards, n)
    
    
