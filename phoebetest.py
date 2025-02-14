import socket
from threading import Thread
from Server import updServer
from GUI import updClient

# the lesson from this test thingy is that join is not good, don't use, and also
# if the server socket truly runs forever, the os thing throws an error. i'm going
# to try to do a thing where it's like if you haven't had a message in a few seconds,
# stop?

#make a client socket
cs = updClient.ClientSocket()

#change the port for the client socket
cs.changeNetwork("127.0.0.1", 7501)

#make a server socket and thread
try:
    ss = updServer.ServerSocket()
    backThread = Thread(target = ss.runServer)
    #cs.sendClientMessage("1")
    backThread.start()
    #backThread.join()
    print("i am interrupting flow")
    print("i am interrupting more")
    cs.sendClientMessage("2")
    print("again")
    cs.sendClientMessage("3")
    cs.sendClientMessage("stop")
    #backThread.join()
except Exception as e:
    print("you dumb fuck ", e)
finally:
    print("closing")
    cs.closeSocket()
    ss.closeSocket()

#see if it works?