import itertools

class InputSets:
    def tf():
        @staticmethod
        return set(True, False)
    
    def handCardSet(gameState, number = 'ALL'):
        @staticmethod
        hand = gameState.pcards[gameState.turn].hand;
        handCards = itertools.chain.from_iterable
                        ((itertools.repeat(c, hand.cards[c]) for c in hand.cards))
        
        if number == 'ALL':
            return itertools.chain.from_iterable
                        ([itertools.combinations(handCards, i) for i in range(hand.size + 1)])
        else:
            return itertools.combinations(handCards, number)
    
