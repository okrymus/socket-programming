$HOW TO RUN THE CODE$

$TorrentClient$
python3 TorrentClient.py P2P pear.cs.umass.edu 19876
python3 TorrentClient.py CS pear.cs.umass.edu 18765

$AUTOGRADE$
python3 auto-grade.py P2P
python3 auto-grade.py CS

$CS with Defult server and port #$
python3 CS.py

$P2P with Defult server and port #$
python3 P2P.py

Goal: Your goal is to write a network program, referred to as the client, that downloads an image file from a server that we maintain. The client must implement two options:
Client/server option: Request the server for the entire file similar to HTTP.
Peer-to-peer option: Request the server for addresses of other peers that possess parts of the file, called blocks, and download these blocks from different peers.
Your client needs to download the image as fast as possible. Note that the first option will not yield the fastest download as the server  (as well as each of the individual peers) services requests at a constrained rate, so relying on only one server (or peer) to get the entire file is likely to yield a poor download rate.

Project assignment https://people.cs.umass.edu/~arun/453/PA2/PA2.html