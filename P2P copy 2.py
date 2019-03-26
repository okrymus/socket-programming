from socket import *
import sys
from CS import *
import random
import threading
import time
import math


# print(sys.path)

lst = []
IsActivePeers = []

def P2P(serverName,serverPort,filename):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message =  'GET '+filename+'.torrent\n'
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    response, serverAddress = clientSocket.recvfrom(2048)
    print(response.decode())

    MAX_PEERS= 8
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
    
    lst = [False for i in range(NUM_BLOCKS)]
    print(lst)

    IsActivePeers = ['inactive' for i in range(len(peers_IP)) ]
 
    threads = []
    
    start_time = time.time()
    iterate = 0
    while(False in lst):
        if (IsActivePeers.count('inactive') > 0):
            peers = random.sample([i for i, e in enumerate(IsActivePeers) if e == 'inactive'],IsActivePeers.count('inactive'))
            for i in peers:
                IsActivePeers[i] = 'active'
                d = DownThread(peers_IP[i],peers_PORT[i],i,filename)
                threads.append(d)
                d.start()
        else:
            if ((IsActivePeers.count('active') + IsActivePeers.count('inactive')) < MAX_PEERS):
                # print(round(elapsed_time)% 5)
                    # clientSocket = socket(AF_INET, SOCK_DGRAM)
                time.sleep(3)
                clientSocket = socket(AF_INET, SOCK_DGRAM)
                message =  'GET '+filename+'.torrent\n'
                clientSocket.sendto(message.encode(),(serverName, serverPort))
                response, serverAddress = clientSocket.recvfrom(2048)
                header = response.split(b'\n')
                addIP = ''
                reduplicate = False
                for h in header:
                    if  ((IsActivePeers.count('active') + IsActivePeers.count('inactive')) < MAX_PEERS):
                        if b'IP' in h:
                            if h.split(b' ')[1].split(b'/')[1].decode() in peers_IP:
                                addIP = h.split(b' ')[1].split(b'/')[1].decode() 
                            else:
                                peers_IP.append(h.split(b' ')[1].split(b'/')[1].decode())
                        if b'PORT' in h:
                            if len(peers_IP) > len(peers_PORT):
                                peers_PORT.append(int(h.split(b' ')[1].decode()))
                                IsActivePeers.append('inactive')
                            else:
                                for i in [i for i, e in enumerate(peers_IP) if e == addIP]:
                                    if peers_PORT[i] is int(h.split(b' ')[1].decode()):
                                        reduplicate = True
                                if not reduplicate:
                                    peers_IP.append(addIP)
                                    peers_PORT.append(int(h.split(b' ')[1].decode()))
                                    IsActivePeers.append('inactive')
                                reduplicate = False
                                addIP = ''                 
                
                    clientSocket.close()
                    # iterate+=1
                    # print(peers_IP)
                    # print("countpoty",len(peers_PORT))
    print("Finish")
    print(len(peers_IP))
    for t in threads:
        t.join(timeout=1)

       
    
    # for i in random.sample(range(81),81):
    #     print(i)
    #     print(lst)
    #     lst[i] = CS('128.119.245.41',6156,"redsox.jpg:"+str(i))

    elapsed_time = time.time() - start_time
    print("Time to download the file: %f"%elapsed_time)

class DownThread(threading.Thread):
    def __init__(self,IP,PORT,i,filename):
        self.IP = IP
        self.PORT = PORT
        self.i = i
        self.filename = filename
        threading.Thread.__init__(self)
        self._content_consumed = False


    def run(self):
        global lst,IsActivePeers
        try:
            if lst.count(False) > 0:
                block = random.sample([i for i, e in enumerate(lst) if e == False],lst.count(False))[0]
                lst[block] = CS(self.IP,self.PORT,self.filename+':'+str(block))
            print(lst.count(False))
            IsActivePeers[self.i]= 'inactive'
        except ConnectionResetError:
            IsActivePeers[self.i] = 'fail'
        # except Exception as e: 
        #     print(e)
        #     IsActivePeers[self.i]= 'inactive'
        #     # IsActivePeers[self.i] = 'fail'

            
        print(IsActivePeers)

 

def main():
    serverName = 'plum.cs.umass.edu'
    serverPort = 19876 
    P2P(serverName,serverPort,"redsox.jpg")

if __name__ == "__main__":
    main()
    