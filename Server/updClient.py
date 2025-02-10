import socket

def send_server_mess_from_client(content):
    msgFromClient       = content
    bytesToSend         = msgFromClient.encode()
    serverAddressPort   = ("127.0.0.1", 7501)
    bufferSize          = 1024

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # try to send data to the server
    try:
        # Send to server using created UDP socket
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        reply = msgFromServer[0]
        #msg = "Message from Server {}".format(msgFromServer[0])

        print("Server replied ", reply)
    except Exception as ex:
        print("unforch your code did not work :(")
        print("some are saying it's bc ", ex)
    finally:
        #close the socket love
        UDPClientSocket.close()
    
send_server_mess_from_client("ur mom")