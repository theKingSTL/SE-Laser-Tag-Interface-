import socket

class ClientSocket:
    #you could change this if you wanted to (to intialize a specific message for example)
    def __init__ (self):
        self.msgFromClient = "No message!"
        self.bytesToSend = self.msgFromClient.encode()
        self.serverAdressPort = ("127.0.0.1", 7500)
        self.bufferSize = 1024
        #self.networkObject = {"network":self.serverAdressPort}

    def sendClientMessage(self, content):
        self.msgFromClient       = content
        self.bytesToSend         = self.msgFromClient.encode()

        # Create a UDP socket at client side
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # try to send data to the server
        try:
            # Send to server using created UDP socket
            UDPClientSocket.sendto(self.bytesToSend, self.serverAddressPort)

            msgFromServer = UDPClientSocket.recvfrom(self.bufferSize)
            reply = msgFromServer[0]
            #msg = "Message from Server {}".format(msgFromServer[0])

            print("Server replied ", reply)
        except Exception as ex:
            print("unforch your code did not work :(")
            print("some are saying it's bc ", ex)
        finally:
            #close the socket love
            UDPClientSocket.close()
    
    def changeNetwork(self, new_ipaddress, new_port):
        ip = str(new_ipaddress)
        self.serverAdressPort = (ip, new_port)

    
    
#send_server_mess_from_client("ur mom")