from CS import CS
from P2P import P2P
import sys

try:
    if (str(sys.argv[1]) == 'CS'):
        serverName = str(sys.argv[2])
        serverPort = int(sys.argv[3])
        CS(serverName,serverPort,"redsox.jpg")
    elif (sys.argv[1] == 'P2P'):
        serverName = str(sys.argv[2])
        serverPort = int(sys.argv[3])
        P2P(serverName,serverPort,"redsox.jpg")
except:
    print("Please enter valid arguments, Example:")
    print("\"python3 TorrentClient.py CS plum.cs.umass.edu 18765\"")





