from socket import *
import time
import sys
import os

def CS(serverName,serverPort,filename):
    BUFFER_SIZE = 1024

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    # clientSocket.settimeout(15)

    # File request 
    getMessage = "GET "+ filename +"\n"

    # send the file request in the following format to the server 
    # to download the file
    
    clientSocket.send(getMessage.encode())

    # Recieve header 
    data = clientSocket.recv(BUFFER_SIZE)
    while b'\n\n' not in data:
        data += clientSocket.recv(BUFFER_SIZE)
        # print(data)
        
    header = data.split(b'\n\n')[0].split(b'\n')
    # print(header)
    data = data.split(b'\n\n')[1]

    # split the header
    if b'200 OK' in header[0]:
        for h in header:
            if b'BODY_BYTE_LENGTH' in h:
                BODY_BYTE_LENGTH = int(h.split(b' ')[1].decode())
            elif b'BODY_BYTE_OFFSET_IN_FILE' in h:
                BODY_BYTE_OFFSET_IN_FILE = int(h.split(b' ')[1].decode())

        # Open the file, ready to write downloaded data in it
        # if file does not exist
        if not os.path.isfile(filename.split(':')[0]):
            f = open(filename.split(':')[0], 'w')
            f.close()

        f = open(filename.split(':')[0],"r+b")

        f.seek(BODY_BYTE_OFFSET_IN_FILE,0)

        if (len(data) is not 0):
            count_bytes = len(data)
            f.write(data)
        else: 
            count_bytes = 0  

        while (count_bytes < BODY_BYTE_LENGTH):
            data = clientSocket.recv(BUFFER_SIZE)
            # print(len(data))
            count_bytes += len(data)
            # write bytes in to the file
            f.write(data)
            print("Filename: " + filename+" Downloaded %d bytes" %count_bytes)
            # print("loca: ",f.tell())
            if not data:
                break

        f.close()
        clientSocket.close()
        return True

    else:
        print(header)
        
    clientSocket.close()

    return False
   

def main():
    serverName = 'pear.cs.umass.edu'
    serverPort = 18765 
    CS(serverName,serverPort,"redsox.jpg")

if __name__ == "__main__":
    main()
    
    
# to know downloadtime
# start_time = time.time()


# elapsed_time = time.time() - start_time
# print("Time to download the file: %f"%elapsed_time)






