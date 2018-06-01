import socket
import select
import threading
import time
import debug
import exceptions
from Player import *
from Table import *

def receive(sock, crlf):
    data = ''
    while not data.endswith(crlf):
        read = sock.recv(1)
        if len(read)<1:
            debug.log('nothing to read: closing socket...')
            close(sock)

        data = data + read
    data = data[:-2]
    debug.log('recieved '+str(sock.getpeername())+': '+str(data))
    return data

def send(sock, data):
    debug.log('sent to '+str(sock.getpeername())+': '+str(data))
    data+='\r\n'
    sock.sendall(data)


def close(sock):
    sock.close()
    if sock in connections:
        connections.remove(sock)
    if sock in players:
        players[sock].Destroy()
        players.pop(sock)


class ClientAcceptThread(threading.Thread):
    def __init__(self, server_socket):
        threading.Thread.__init__(self)
        self.server_socket = server_socket

    def run(self):
        global connections
        global players
        while True:
            connection, client_address = self.server_socket.accept()
            debug.log('Client ' + str(client_address) + ' connected successfully')
            connections.append(connection)
            players[connection] = Player()
            players[connection].SendMessage('hello')



def read_from(client):
    global players
    global connections
    global tables
    try:
        data = receive(client, '\r\n')

        if players[client].state == 'waiting_for_name':
            recieved = str(data)
            if recieved.startswith('name '):
                players[client].name = recieved[5:]
                debug.log('Player\'s name is '+str( players[client].name))
                players[client].SendMessage('received name '+str(players[client].name))
                players[client].state = 'waiting_in_lobby'

        elif players[client].state == 'waiting_in_lobby':
            recieved = str(data)
            if recieved.startswith('req table '):
                request = str(recieved[10:])
                if request.startswith('id '):
                    try:
                        req_id = int(request[3:])
                        print req_id
                        if tables[req_id].IsFull():
                            debug.log('Table' +str(tables[req_id].tableId)+' is full')
                            players[client].msgs.append('table is full')
                        else:
                            players[client].JoinTable(tables[req_id])
                            players[client].state = 'in_game'
                    except Exception as e:
                        debug.log(e)
                        players[client].msgs.append('table not found')

                elif request=='NEW':
                    players[client].JoinTable(CreateTable())
                    players[client].state = 'in_game'

                elif request=='RND':
                    for table in tables:
                        if not table.IsFull():
                            players[client].JoinTable(table)
                            players[client].state = 'in_game'
                            return
                    debug.log('No free tables found')
                    players[client].JoinTable(CreateTable())
                    players[client].state = 'in_game'

        if players[client].state == 'in_game':
            recieved = str(data)
            if recieved == 'return to lobby':
                players[client].LeaveTable()
                players[client] = Player()
                players[client].state = 'waiting_in_lobby'
            elif players[client].active:
                if recieved == 'fold':
                    players[client].Fold()
                elif recieved == 'call':
                    players[client].Call()
                elif recieved.startswith('raise '):
                    try:
                        bet_raise = int(recieved[6:])
                        players[client].Raise(bet_raise)
                    except Exception as e:
                        debug.log(e)


    except Exception as e:
        debug.log(e)
        close(client)


def write_to(client):
    global players
    global connections
    global tables
    data = ''

    try:
        if client in players:
            if len(players[client].msgs) > 0:
                data = str(players[client].msgs.pop(0))
            """
            elif players[client].state == 'connected':
                data = 'hello'
                players[client].state = 'waiting_for_name'
            elif players[client].state == 'received_name':
                data = 'received name '+str(players[client].name)
                players[client].state = 'waiting_in_lobby'
            elif players[client].state == 'connecting_to_table':
                data = 'connecting to table '+str(players[client].name)
                players[client].state = 'waiting_in_lobby'
            """

        if len(data)<1:
            return

        send(client,data)

    except Exception as e:
        debug.log(e)
        close(client)


def CreateTable():
    global tables
    newTable = Table()
    tables.append(newTable)
    return newTable



connections = []
players = {}
tables = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('212.182.27.120', 7700)
sock.bind(server_address)

debug.log('Starting up TCP server on %s port %s' % server_address)

sock.listen(16)
client_accepting_thread = ClientAcceptThread(sock)
client_accepting_thread.start()


while True:
    time.sleep(0.001)
    for table in tables:
        if table.gamestate == 'showdown':
            if table.timer<2:
                table.timer+=0.001
            else:
                table.timer = 0
                table.gamestate = 'waiting_for_players'
                if table.PlayerCount()>1:
                    table.StartGame()

    if len(connections)<1:
        continue
    readable, writeable, exceptional = select.select(connections, connections, connections)
    #debug.log(str(readable) + str(writeable) + str(exceptional))

    #reading data from readable sockets
    for read_connection in readable:
        read_from(read_connection)

    #writing data to all writeable sockets
    for write_conneciton in writeable:
        write_to(write_conneciton)