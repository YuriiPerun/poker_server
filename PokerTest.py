from Player import *
from Hand import *
from Card import *
import select

def fun(a,b):
    return -b, -a

J = 11
Q = 12
K = 13
A = 14


player1 = Player()
player2 = Player()

#Building test hand for player1
player1.hand.cards.append(Card(A,'H'))
player1.hand.cards.append(Card(A,'H'))
player1.hand.cards.append(Card(A,'H'))
player1.hand.cards.append(Card(Q,'H'))
player1.hand.cards.append(Card(Q,'H'))


#Building test hand for player2
player2.hand.cards.append(Card(A,'H'))
player2.hand.cards.append(Card(A,'H'))
player2.hand.cards.append(Card(A,'H'))
player2.hand.cards.append(Card(K,'H'))
player2.hand.cards.append(Card(2,'H'))

print('')
print(player1.hand.cards)
print(player2.hand.cards)
print('')

print(player1.hand > player2.hand)