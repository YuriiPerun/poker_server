from Card import *
import math

combinations = [
    'High Card',
    'One Pair',
    'Two Pair',
    'Three of a Kind',
    'Straight',
    'Flush',
    'Full House',
    'Four of a Kind',
    'Straight Flush',
    'Royal Flush'
]

class Hand(object):
    def __init__(self, **kwargs):
        self.cards = [None, None]
        self.counts = []

    def __cmp__(self, other):
        self_rank, self_power = self.check_combination(self.cards)
        other_rank, other_power = other.check_combination(other.cards)
        #print str(combinations[self_rank])+' :: '+str(combinations[other_rank])
        #print str(self_power)+' :: '+str(other_power)

        if self_rank != other_rank:
            return  self_rank - other_rank
        else:
            return self_power-other_power

    def __str__(self):
        returned_str = ''
        for card in self.cards:
            if card:
                returned_str += ' ' + str(card.index())
            else:
                returned_str += ' None'
        return returned_str



    def AddCard(self, card):
        for i in range(len(self.cards)):
            if not self.cards[i]:
                self.cards[i] = card


    def check_combination(self, combination):
        my_cards = sorted(combination)
        self.counts = []
        present = []
        for i in range(15):
            self.counts.append(0)
            present.append(False)
        for card in my_cards:
            self.counts[card.value] += 1
            present[card.value] = True
            if card.value == 14:
                present[1] = True

        sequential = False
        i = 1
        sequence_length = 0
        while i < 15:
            if present[i]:
                sequence_length += 1
            else:
                sequence_length = 0
            if sequence_length>=5:
                sequential = True
                break
            i+=1

        same_suit = True
        i = 0
        while i < 4:
            same_suit = same_suit and (my_cards[i].suit == my_cards[i + 1].suit)
            i += 1

        """
        print
        print 'card counted: '+str(self.counts)
        print 'sequential? = '+str(sequential)
        print 'same suit? = '+str(same_suit)
        print
        """

        # Pattern is the following:
        # return RANK, POWER

        if sequential and same_suit:
            if my_cards[-1].value == 14 and my_cards[-2].value == 13:
                return 9, 0
            else:
                power = 0
                if my_cards[0].value == 2 and my_cards[-1].value == 14:
                    power = 1
                else:
                    power = combination[0]
                return  8, power


        power = 0
        found_4_same = False
        for i in range(15):
            if self.counts[i]==1:
                power += i
            if self.counts[i]==4:
                power += i * 100
                found_4_same = True
        if found_4_same:
            return  7, power


        power = 0
        found_3_same = False
        found_2_same = False
        for i in range(15):
            if self.counts[i]==3:
                found_3_same = True
                power += 10000 * i
            elif self.counts[i]==2:
                found_2_same = True
                power += 100 * i
            if found_2_same and found_3_same:
                return 6, power

        if same_suit:
            power = 0
            for i in range(5):
                power += my_cards[i].value * (100**i)
            return 5, power

        if sequential:
            power = 0
            if my_cards[0].value == 2 and my_cards[-1].value == 14:
                power = 1
            else:
                power = combination[0]
            return  4, power


        found_3_same = False
        multiplier = 1
        power = 0
        for i in range(15):
            if self.counts[i]==3:
                found_3_same = True
                power += i * 10000
        if found_3_same:
            for i in range(5):
                if self.counts[i]<3:
                    power += my_cards[i].value * multiplier
                    multiplier *= 100
            return 3, power


        found_2_same = False
        found_2_pair = False
        power = 0
        for i in range(15):
            if self.counts[i]==1:
                power+=i
            elif self.counts[i]==2:
                if not found_2_same:
                    found_2_same = True
                    power += i * 100
                else:
                    found_2_pair = True
                    power += i * 10000
        if found_2_pair:
            return 2, power


        found_2_same = False
        multiplier = 1
        power = 0
        for i in range(15):
            if self.counts[i]==2:
                found_2_same = True
                power += i * 1000000
        if found_2_same:
            for i in range(5):
                if self.counts[i]<2:
                    power += my_cards[i].value * multiplier
                    multiplier *= 100
            return 1, power

        power = 0
        for i in range(5):
            power += my_cards[i].value * (100**i)
        return 0, power
