from Player import Player
from sys import stdin
_magicString = 'Choose an option, p being print statistics and hand'
_noop = ', with -1 being none of the above'

def _iterateAndAsk(lst, noop=False):
    for item in enumerate(lst):
        print item
    option = None
    if noop:
        option = raw_input(_magicString+_noop+':')
    else:
        option = raw_input(_magicString+':')
    return option


class Human_Player(Player):
    def selectInput(self, inputs, gameState, actionSimulator=None,
            helpMessage=None):
        print helpMessage
        option = _iterateAndAsk(inputs)
        if option == 'p':
            print gameState.abcs[gameState.turn]
            print '\n'
            print gameState.pcards[gameState.turn].hand
        else:
            option = int(option)
            return inputs[option]

    def playActionPhase(self, gameState):
        gameState = gameState.clone()
        pcards = gameState.pcards[gameState.turn]
        abcs = gameState.abcs[gameState.turn]
        cards = self.availableActions(gameState)
        while cards:
            option = _iterateAndAsk(cards, True)
            if option == '-1':
                break
            elif option == 'p':
                print abcs, pcards.hand
                continue
            else:
                i = int(option)
                gameState.pcards[gameState.turn].discardFromHand(cards[i])
                gameState.abcs[gameState.turn]['actions'] -= 1
                gameState = cards[i].action(gameState)
                cards[i] = availableActions(self, gameState)
        return gameState

    def playBuyPhase(self, gameState):
        gameState = gameState.clone()
        pcards = gameState.pcards[gameState.turn]
        abcs = gameState.abcs[gameState.turn]
        buys = gameState.abcs[gameState.turn]['buys']
        coins = gameState.abcs[gameState.turn]['coins'] + self.totalTreasure(gameState)
        while buys > 0:
            possibleBuys = self.availableBuys(gameState, coins)
            option = _iterateAndAsk(possibleBuys, True)
            if option == '-1':
                break
            elif option == 'p':
                print abcs, pcards.hand
                continue
            else:
                i = int(option)
                gameState.stacks[possibleBuys[i]] -= 1
                buys -= 1
                coins -= possibleBuys[i].cost
                pcards.gain(possibleBuys[i])
        gameState.abcs[gameState.turn]['buys'] = buys
        gameState.abcs[gameState.turn]['coins'] = coins
        return gameState

    def playDiscardPhase(self, gameState):
        gameState = gameState.clone()
        gameState.pcards[gameState.turn].discardPhase()
        return gameState
