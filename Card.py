suit_indices = {'C':0,'S':1,'D':2,'H':3}
suits = ['C','S','D','H']

class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __cmp__(self, other):
        return self.value - other.value

    def index(self):
        i = 0
        if self.value == 14:
            i = 1
        else:
            i = self.value
        i += suit_indices[self.suit]*13
        return i

    def __repr__(self):
        value_string = ''
        if self.value==11:
            value_string = 'J'
        elif self.value == 12:
            value_string = 'Q'
        elif self.value == 13:
            value_string = 'K'
        elif self.value == 14:
            value_string = 'A'
        else:
            value_string = str(self.value)
        return value_string+str(self.suit)
