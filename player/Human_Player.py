from Player import Player
from sys import stdin
_magicString = 'Choose an option, p being print statistics, d discard'
_noop = ', with \'\' being none of the above'

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
def _iterateAndAsk(lst, noop=False):
    for item in enumerate(lst):
        print str(item[0]) + ': ' + str(item[1])
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
        inputs = list(inputs)
        if len(inputs) == 0:
            return None
        option = _iterateAndAsk(list(inputs))
        if option == 'p':
            print_fancy_state(gameState)
        elif option == 'd':
            print_discard(gameState)
        else:
            i = int(option)
            return inputs[i]

    def playActionPhase(self, gameState):
        gameState = gameState.clone()
        cards = self.availableActions(gameState)
        while cards:
            card_names = [card.name for card in cards]
            option = _iterateAndAsk(card_names, True)
            if option == '-1' or option == '':
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
                cards = self.availableActions(gameState)
        return gameState

    def playBuyPhase(self, gameState):
        gameState = gameState.clone()
        pcards = gameState.pcards[gameState.turn]
        abcs = gameState.abcs[gameState.turn]
        abcs['coins'] += self.totalTreasure(gameState)
        while abcs['buys'] > 0:
            possibleBuys = self.availableBuys(gameState, abcs['coins'])
            buy_names = [card.name +': '+str(card.cost)+': '+str(gameState.stacks[card])+' remaining.' for card in possibleBuys]
            option = _iterateAndAsk(buy_names, True)
            if option == '-1' or option == '':
                break
            elif option == 'p':
                print_fancy_state(gameState,messg='It is the Buy Phase')
            elif option == 'd':
                print_discard(gameState)
            else:
                i = int(option)
                gameState.stacks[possibleBuys[i]] -= 1
                abcs['buys'] -= 1
                abcs['coins'] -= possibleBuys[i].cost
                pcards.gain(possibleBuys[i])
        return gameState

    def playDiscardPhase(self, gameState):
        gameState = gameState.clone()
        gameState.pcards[gameState.turn].discardPhase()
        return gameState
