import socket

class ClientSocket:
    #you could change this if you wanted to (to intialize a specific message for example)
    def __init__ (self):
        self.msgFromClient = "No message!"
        self.bytesToSend = self.msgFromClient.encode()
        self.serverAddressPort = ["127.0.0.1", 7500]
        self.bufferSize = 1024
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def sendClientMessage(self, content):
        # Create a UDP socket at client side
        # try to send data to the server
        try:
            # Send to server using created UDP socket
            self.UDPClientSocket.sendto(str.encode(str(content)), (self.serverAddressPort[0],self.serverAddressPort[1]))
            print(f"Sent content: {content} to {self.serverAddressPort[1]}")
        except Exception as ex:
            print("unforch your code did not work bc ", ex)
    
    def changeNetwork(self, new_ipaddress):
        ip = str(new_ipaddress)
        self.serverAddressPort[0] = ip

