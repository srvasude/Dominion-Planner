from Player import Player
from sys import stdin
_magicString = 'Choose an option, p being print statistics, d discard'
_noop = ', with -1 being none of the above'

def print_fancy_state(gameState, messg=None):
    print 'It is currently your turn '+str(gameState.turn) +'.'
    if messg:
        print messg
    abcs = gameState.abcs[gameState.turn]
    print 'You have '+ str(abcs['actions']) + ' actions' +' and ' + str(abcs['buys']) + ' buys left'
    print 'These are the cards in your hand:'
    pcards = gameState.pcards[gameState.turn]
    for card in pcards.hand:
        print card.name + ': ' + str(pcards.hand[card])
    totCards = pcards.hand.count + pcards.discard.count + pcards.deck.count
    print 'You have a total of ' + str(totCards) + ' cards.'

def print_discard(gameState):
    for card in gameState.pcards[gameState.turn].discard:
        print card.name + ': ' + str(gameState.pcards[gameState.turn].discard[card])
def _iterateAndAsk(lst, noop=False, cards=False):
    for item in enumerate(lst):
        if cards:
            print str(item[0]) + ' ' + item[1].name + ': ' + str(item[1].cost)
        else:
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
            print_fancy_state(gameState)
        elif option == 'd':
            print_discard(gameState)
        else:
            i = int(option)
            return inputs[i]

    def playActionPhase(self, gameState):
        gameState = gameState.clone()
        pcards = gameState.pcards[gameState.turn]
        abcs = gameState.abcs[gameState.turn]
        cards = self.availableActions(gameState)
        while cards:
            option = _iterateAndAsk(cards, True, True)
            if option == '-1':
                break
            elif option == 'p':
                print_fancy_state(gameState,messg='It is the Action Phase')
            elif option == 'd':
                print_discard(gameState)
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
            option = _iterateAndAsk(possibleBuys, True, True)
            if option == '-1':
                break
            elif option == 'p':
                print_fancy_state(gameState,messg='It is the Buy Phase')
            elif option == 'd':
                print_discard(gameState)
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
