#!/usr/bin/env python
import socket
import time
import threading

HOST = '192.168.0.41'
PORT = 7700
server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.connect(server_address)

print "name test_client_"+str(sock.getsockname()[1])
sock.send("name test_client_"+str(sock.getsockname()[1])+'\r\n')
sock.send("req table RND\r\n")
sock.send("return to lobby\r\n")
time.sleep(5)