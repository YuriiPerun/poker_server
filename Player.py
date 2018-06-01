import debug
from Hand import *


class Player(object):
    count = 0

    def __init__(self):
        self.player_id = Player.count
        self.name = ''
        self.money = 4000
        self.bet = 0
        self.playing = False
        self.active = False

        self.state = "waiting_for_name"
        self.reading = True

        self.msgs = []
        self.req_table = ''

        self.table = None
        self.hand = Hand()
        self.bestHand = Hand()
        Player.count += 1
        debug.log('Player #' + str(self.player_id) + ' created')

    def __del__(self):
        debug.log('Player #' + str(self.player_id) + ' destroyed')

    def is_better_than(self, other):
        return self.bestHand.__cmp__(other.bestHand)

    def Destroy(self):
        self.LeaveTable()
        debug.log('Player #' + str(self.player_id) + ' destroying...')
        del self

    def SendMessage(self, message):
        self.msgs.append(str(message))





    def JoinTable(self, table):
        debug.log('Player #' + str(self.player_id) + ' joins table ' + str(table.tableId))
        self.table = table
        self.SendMessage('connecting to table ' + str(table.tableId))
        table.AddPlayer(self)
        self.RefreshTable()

    def LeaveTable(self):
        if not self.table:
            return
        self.table.RemovePlayer(self)
        debug.log('Player #' + str(self.player_id) + ' leaves table ' + str(self.table.tableId))
        self.table = None

    def RefreshTable(self):
        if not self.table:
            return
        self.table.RefreshAll()




    def Bet(self, bet):
        self.bet += bet
        self.money -= bet

    def Fold(self):
        if not self.playing or not self.table:
            return
        self.playing = False
        self.bet = 0
        for pool in self.table.pools:
            if self in pool.players:
                pool.players.remove(self)
        self.EndTurn()

    def Raise(self, bet_add):
        if not self.playing or not self.table:
            return
        if bet_add > self.money:
            bet_add = self.money
        elif bet_add < self.table.current_bet-self.bet:
            return
        #elif bet_add < self.table.big_blind and not bet_add == self.table.current_bet-self.bet:
        #    return
        self.money -= bet_add
        self.bet += bet_add
        self.EndTurn()

    def Call(self):
        self.Raise(self.table.current_bet-self.bet)

    def EndTurn(self):
        self.table.EndTurn()

    def CalculateHand(self):
        totalHand = []
        totalHand.extend(self.hand.cards)
        totalHand.extend(self.table.table_cards)
        self.bestHand = Hand()
        self.bestHand.cards = [totalHand[0], totalHand[1], totalHand[2], totalHand[3], totalHand[4]]
        for i in range(6):
            for j in range(i+1,7):
                newHand = Hand()
                newHand.cards = []
                for k in range(7):
                    if k != i and k != j:
                        newHand.cards.append(totalHand[k])
                if newHand > self.bestHand:
                    self.bestHand = newHand

