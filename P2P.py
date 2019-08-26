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
peers_IP = []
peers_PORT = []
MAX_PEERS= 6
count_process_add_peer = 0


def P2P(serverName,serverPort,filename):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message =  'GET '+filename+'.torrent\n'
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    response, serverAddress = clientSocket.recvfrom(2048)
    print(response.decode())

    global lst, IsActivePeers, peers_IP, peers_PORT,count_process_add_peer
    
    # get information such as NUM_BLOCKS, FILE_SIZE and PEER Addresses and port nummbers
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
    
    # lst will tell us that which blocks downloaded and haven't been downloaded yet
    lst = [False for i in range(NUM_BLOCKS)]
    print(lst)

    # set all peers is inactive which mean it is ready to creat a new connection
    IsActivePeers = ['inactive' for i in range(len(peers_IP)) ]
 
    threads = []
    
    start_time = time.time()
    count_process_add_peer = 0
    while(False in lst):
        if (IsActivePeers.count('inactive') > 0):
            # Randonly pick the number of block that has not downloaded
            peers = random.sample([i for i, e in enumerate(IsActivePeers) if e == 'inactive'],IsActivePeers.count('inactive'))
            # Use multiple thread to connect each peer and download multiple blocks as the same time
            for i in peers:
                # the peer is in used, so let label it 'active' peer
                IsActivePeers[i] = 'active'
                d = DownThread(peers_IP[i],peers_PORT[i],i,filename)
                threads.append(d)
                d.start()

        # To get more peers, only allow one process to add more peers
        # the number of peers will not exceed MAX_PEERS
        if ((IsActivePeers.count('active') + IsActivePeers.count('inactive')) < MAX_PEERS) and (count_process_add_peer < 1):
            count_process_add_peer += 1
            p = GetPeers(serverName,serverPort,filename)
            threads.append(p)
            p.start()
        print("Downloaded %d blocks" %(NUM_BLOCKS-lst.count(False)))
        
    
    print("Finish")
    # print(len(peers_IP))
    for t in threads:
        t.join(timeout=1)

    elapsed_time = time.time() - start_time
    print("Time to download the file: %f"%elapsed_time)

class GetPeers(threading.Thread):
    def __init__(self,serverName, serverPort,filename):
        self.serverName = serverName
        self.serverPort = serverPort
        self.filename = filename
        threading.Thread.__init__(self)
        self._content_consumed = False


    def run(self):
        global lst, IsActivePeers, peers_IP, peers_PORT,count_process_add_peer
        serverName = self.serverName 
        serverPort = self.serverPort
        filename = self.filename 

        while ((IsActivePeers.count('active') + IsActivePeers.count('inactive')) < MAX_PEERS and lst.count(False) > (IsActivePeers.count('active') + IsActivePeers.count('inactive')) ):    
            # since the sever do not allow to ask for new peers very fast
            # let the process wait for the server a litle bit 
            time.sleep(3)
            clientSocket = socket(AF_INET, SOCK_DGRAM)
            message =  'GET '+filename+'.torrent\n'
            clientSocket.sendto(message.encode(),(serverName, serverPort))
            response, serverAddress = clientSocket.recvfrom(2048)
            header = response.split(b'\n')
            addIP = ''
            reduplicate = False
            # get new peers from the header. New peer must not duplcated and not exceed the limit number of peers
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
        count_process_add_peer-=1


# Downloading thread
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
                # use CS function from CS.py to download each block
                lst[block] = CS(self.IP,self.PORT,self.filename+':'+str(block))
            IsActivePeers[self.i]= 'inactive'
        # except ConnectionResetError:
        #     IsActivePeers[self.i] = 'fail'
        # except ConnectionRefusedError:
        #     IsActivePeers[self.i] = 'fail'
        # handle error from connection
        except Exception as e: 
            print(e)
            lst[block] =  False
            IsActivePeers[self.i] = 'fail'
        
        print("Peers status:"+str(IsActivePeers))
        # print(threading.active_count())

 

def main():
    serverName = 'pear.cs.umass.edu'
    serverPort = 19876 
    P2P(serverName,serverPort,"Redsox.jpg")

if __name__ == "__main__":
    main()
    