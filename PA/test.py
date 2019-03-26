from socket import *
import sys
from CS import * 
import random
import threading
import time


def P2P(serverName,serverPort,filename):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message =  'GET '+filename+'.torrent\n'
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    response, serverAddress = clientSocket.recvfrom(2048)
    print(response.decode())

    MAX_PEERS= 4
    peers_IP = []
    peers_PORT = []
    global lst,IsActivePeers
    
    header = response.split(b'\n')
    for h in header:
        if b'NUM_BLOCKS' in h:
            NUM_BLOCKS = int(h.split(b' ')[1])
        if b'FILE_SIZE' in h:
            FILE_SIZE = int(h.split(b' ')[1])
        if b'IP' in h:
            peers_IP.append(h.split(b' ')[1].split(b'/')[1].decode())
        if b'PORT' in h:
            peers_PORT.append(int(h.split(b' ')[1].decode()))

    clientSocket.close()

def main():
    serverName = 'plum.cs.umass.edu'
    serverPort = 19876 
    P2P(serverName,serverPort,"redsox.jpg")
    time.sleep(3)
    P2P(serverName,serverPort,"redsox.jpg")
    time.sleep(3)
    P2P(serverName,serverPort,"redsox.jpg")



if __name__ == "__main__":
    main()
    