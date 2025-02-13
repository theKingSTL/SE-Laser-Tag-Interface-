import socket

#phoebe comments as i try to understand upd, feel fry to ignore <3

#so the instructions say that every time a player is added, i should transmit their equipment id
#i'm making the method right now, but i feel like it defnitely has to be called within the main function
#as a thought

localIP     = "127.0.0.1"
#he also wants an option to "change the network" which i'm guessing means either changing IP or port or both
localPort   = 7501
bufferSize  = 1024
#so this looks like what we are sending the client (and i guess we have to encode?)
msgFromServer       = "Hello UDP Client"
bytesToSend         = msgFromServer.encode()

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")
repeat = 0

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)

    #repeat += 1
    #if (repeat == 100):
        #me trying to stop the server (and it just not working <3)
        #answer = input("should i stop")
        #if (answer == "y"):
            #break

