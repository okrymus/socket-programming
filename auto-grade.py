from socket import *
import time
from CS import CS
from P2P import P2P
import sys

def computeXORChecksum(filename):
    jpeg = open(filename,'rb')
    fileBytes = jpeg.read()
    jpeg.close()
    i = 0
    words = [0,0,0,0,10]
    while i < len(fileBytes):
        if i%4 == 0:
            words[0] = words[0]^fileBytes[i]
        elif i%4 == 1:
            words[1] = words[1]^fileBytes[i]
        elif i%4 == 2:
            words[2] = words[2]^fileBytes[i]
        elif i%4 == 3:
            words[3] = words[3]^fileBytes[i]
        i+=1
    checksum = bytes([words[0],words[1],words[2],words[3],words[4]])
    return checksum+b'\n'


def main():
    # Grading server
    serverName = 'date.cs.umass.edu'
    serverPort = 20001
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    # command message
    getMessage = "IAM 31526077\n"

    clientSocket.send(getMessage.encode())

    # Recieve header 
    data = clientSocket.recv(1024)
    print(data.decode())
    
    filename="31526077_redsox.jpg"

    try: 
        # test with PA1 client/server
        if (str(sys.argv[1])=='CS'):
            CS('date.cs.umass.edu',18765,filename)
            # compute XOR Checksum
            clientSocket.send(computeXORChecksum(filename))
            data = clientSocket.recv(1024)
            print(data.decode())
            clientSocket.close()
        elif (str(sys.argv[1])=='P2P'):
            P2P('date.cs.umass.edu',19876,filename)
            # compute XOR Checksum
            clientSocket.send(computeXORChecksum(filename))
            data = clientSocket.recv(1024)
            print(data.decode())
            clientSocket.close()
    except:
        print("Invalid argument try this:")
        print("python3 auto-grade.py CS")
    

if __name__ == "__main__":
    main()
    
    


# filename="31526077_redsox.jpg"
# clientSocket.send(computeXORChecksum(filename))

# data = clientSocket.recv(1024)
# print(data)

# clientSocket.close()




