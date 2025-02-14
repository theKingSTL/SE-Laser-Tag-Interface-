import socket
import threading

class ServerSocket:
    def __init__(self):
        self.localIP     = "127.0.0.1"
        self.localPort   = 7501
        self.bufferSize  = 1024
        self.msgFromServer       = "Client message received!"
        self.bytesToSend         = self.msgFromServer.encode()

        # Create a datagram socket
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip
        self.UDPServerSocket.bind((self.localIP, self.localPort))

        print("UDP server up and listening")

    # Listen for incoming datagrams

    def runServer(self):
        while(True):
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            clientMsg = "Message from Client:{}".format(message)
            clientIP  = "Client IP Address:{}".format(address)
            
            print(clientMsg)
            print(clientIP)

            if ("stop" in clientMsg):
                break

            # Sending a reply to client
            #this just replies, and i believe it only sends 
            #if a message is received. potentially fix (also i don't think client is set up to receive so nvm)
            #self.UDPServerSocket.sendto(self.bytesToSend, address)

    def closeSocket(self):
        self.UDPServerSocket.shutdown(socket.SHUT_RDWR)
        self.UDPServerSocket.close()
