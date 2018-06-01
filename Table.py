import debug
import random
from array import *
from Player import *
from Hand import *

class Pool(object):
    def __init__(self):
        self.players = []
        self.money = 0

    def __repr__(self):
        return str(self.money)




class Table(object):
    count = 0

    def __init__(self):
        self.tableId = Table.count
        self.players = [None, None, None, None, None, None]
        self.table_cards = [None,None,None,None,None]
        self.pools = []
        self.cards = []

        self.small_blind = 10
        self.big_blind = 20
        self.current_bet = 0
        self.start_index = 0
        self.current_active_index = 0
        self.last_raise_index = 0

        self.timer = 0.0
        self.gamestate = 'waiting_for_players'

        Table.count += 1
        debug.log('Table #' + str(self.tableId) + ' created')

    def __del__(self):
        debug.log('Table #' + str(self.tableId) + ' destroyed')



    def AddPlayer(self, newPlayer):
        for i in range(len(self.players)):
            if not self.players[i]:
                self.players[i] = newPlayer
                break
        if self.PlayerCount()>1 and self.gamestate=='waiting_for_players':
            self.StartGame()

    def RemovePlayer(self, player):
        if not player in self.players:
            return
        player.Fold()
        self.players[self.players.index(player)] = None
        if self.CountPlaying()<2:
            self.EndGame()
        else:
            self.RefreshAll()



    def PlayerCount(self):
        player_count = 0
        for i in range(len(self.players)):
            if self.players[i]:
                player_count+=1
        return  player_count

    def CountPlaying(self):
        player_count = 0
        for i in range(len(self.players)):
            if self.players[i] and self.players[i].playing:
                player_count+=1
        return  player_count

    def IsFull(self):
        return self.PlayerCount()>=6




    def RefreshAll(self):
        for player in self.players:
            if player:
                self.Refresh(player)

    def Refresh(self, player_refreshing):
        player_info = 'refresh self '+str(player_refreshing.active) + ' '+str(player_refreshing.money)+' '+str(player_refreshing.bet) +' '+ str(self.current_bet)
        player_refreshing.SendMessage(player_info)

        for i in range(len(self.players)):
            player = self.players[i]
            if not player:
                message = 'refresh player ' + str(i) + ' ' + str(player)
            else:
                message = 'refresh player '+str(i)+' '+ player.name+' '+str(player.money)+' '+str(player.bet) + \
                      ' '+str(player.playing)+' '+str(player.active)
                if player == player_refreshing or self.gamestate == 'showdown':
                    message += str(player.hand)
                elif not player.playing:
                    message += ' None None'
                else:
                    message += ' 0 0'
            player_refreshing.SendMessage(message)

        cards_message = 'refresh cards'
        for card in self.table_cards:
            if card:
                cards_message += ' ' + str(card.index())
            else:
                cards_message += ' None'
        player_refreshing.SendMessage(cards_message)

        pools_message = 'refresh pools'
        for pool in self.pools:
            pools_message += ' '+str(pool)
        player_refreshing.SendMessage(pools_message)



    def StartGame(self):
        debug.log('Table #' + str(self.tableId) + ' started game')
        self.pools = []
        self.table_cards = [None,None,None,None,None]
        self.GenerateCards()

        self.gamestate = 'preflop'
        for player in self.players:
            if player:
                player.bet = 0
                player.bet = 0
                player.playing = True
                player.active = False
                player.hand.cards[0] = self.GetRandomCard()
                player.hand.cards[1] = self.GetRandomCard()

        self.current_active_index = self.NextIndex(self.start_index)
        self.current_active_index = self.NextIndex(self.current_active_index)
        self.players[self.current_active_index].active = True
        count = 0
        while not self.players[self.start_index]:
            self.start_index = self.NextIndex(self.start_index)
        i = self.start_index
        player = self.players[i]
        while count < 2:
            player = self.players[i]
            i = self.NextIndex(i)
            if count == 0:
                player.Bet(self.small_blind)
            elif count == 1:
                player.Bet(self.big_blind)
            count+=1

        self.current_bet = self.big_blind
        self.RefreshAll()


    def EndGame(self):
        self.gamestate = 'showdown'
        winners = []
        if self.CountPlaying()>1:
            for player in self.players:
                if player and player.playing:
                    player.CalculateHand()

                    rank = player.bestHand.check_combination(player.bestHand.cards)[0]
                    print str(combinations[rank])



            for pool in self.pools:
                hands=[]
                for player in pool.players:
                    hands.append(player.bestHand)
                winner_hand = (sorted(hands))[-1]

                for i in range(len(self.players)):
                    if not self.players[i]:
                        continue
                    if self.players[i].bestHand is winner_hand:
                        self.players[i].money += pool.money
                        pool.money = 0
                        winners.append(i)
                        break
        else:
            for i in range(len(self.players)):
                if self.players[i]:
                    winners.append(i)
                    break

        for player in self.players:
            if player:
                player.active = False
                player.playing = False
        self.RefreshAll()
        for winner in winners:
            for player in self.players:
                if player:
                    endgame_message = 'set winner '+str(winner)
                    player.SendMessage(endgame_message)
        debug.log('Table #' + str(self.tableId) + ' ended game')




    def InitiatePhase(self):
        i = self.start_index
        for player in self.players:
            if player:
                player.bet = 0
        self.current_bet = 0
        self.start_index = self.NextIndex(self.start_index)
        self.players[self.current_active_index].active = False
        self.current_active_index = self.start_index
        self.last_raise_index = self.start_index
        self.players[self.current_active_index].active = True
        self.RefreshAll()

    def EndPhase(self):
        self.CheckBets()
        if self.gamestate == 'preflop':
            self.gamestate = 'flop'
            self.table_cards[0] = self.GetRandomCard()
            self.table_cards[1] = self.GetRandomCard()
            self.table_cards[2] = self.GetRandomCard()
        elif self.gamestate == 'flop':
            self.gamestate = 'turn'
            self.table_cards[3] = self.GetRandomCard()
        elif self.gamestate == 'turn':
            self.gamestate = 'river'
            self.table_cards[4] = self.GetRandomCard()
        elif self.gamestate == 'river':
            self.EndGame()
            return
        self.InitiatePhase()


    def NextIndex(self, index):
        next_index = (index + 1) % len(self.players)
        while not (self.players[next_index] and self.players[next_index].playing):
            next_index = (next_index + 1) % len(self.players)
        return next_index

    def EndTurn(self):
        if self.CountPlaying()<2:
            self.EndGame()
            return
        if self.players[self.current_active_index].bet > self.current_bet:
            self.current_bet = self.players[self.current_active_index].bet
            self.last_raise_index = self.current_active_index
        if self.NextIndex(self.current_active_index) == self.last_raise_index and\
            self.players[self.NextIndex(self.current_active_index)].bet == self.players[self.current_active_index].bet:
            self.EndPhase()
        else:
            self.players[self.current_active_index].active = False
            self.current_active_index = self.NextIndex(self.current_active_index)
            self.players[self.current_active_index].active = True
            self.RefreshAll()


    def CheckBets(self):
        if len(self.pools)<1:
            self.CreateNewPool()
        totalbet = 0
        for player in self.players:
            if player:
                totalbet += player.bet

        while totalbet > 0:
            lastPool = self.pools[-1]
            min_bet = 0
            for player in self.players:
                if not player or player.bet <= 0:
                    continue
                if player.bet < min_bet or min_bet==0:
                    min_bet = player.bet
            for player in self.players:
                if not player or player.bet <= 0:
                    continue
                lastPool.money += min_bet
                player.bet -= min_bet
                totalbet -= min_bet
            if totalbet > 0:
                self.CreateNewPool()



    def CreateNewPool(self):
        self.pools.append(Pool())
        for player in self.players:
            if player and player.bet > 0:
                self.pools[-1].players.append(player)

    def GenerateCards(self):
        for index in range(4):
            suit = suits[index]
            for value in range(13):
                newcard = Card(value+2,suit)
                self.cards.append(newcard)

    def GetRandomCard(self):
        return self.cards.pop(random.randrange(0,len(self.cards)))