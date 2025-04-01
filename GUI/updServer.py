import socket
from threading import Thread, Event

class ServerSocket:
    def __init__(self):
        self.localIP     = "127.0.0.1"
        self.localPort   = 7501
        self.bufferSize  = 1024
        self.msgFromServer = "Client message received!"
        self.messageQueue = []  # Store received messages

        # This event lets the thread know when it should stop
        self.stop_event = Event()

        self.UDPServerSocket = None
        self.backThread = None

    def startServer(self):    
        # Create a datagram socket
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip
        self.UDPServerSocket.bind((self.localIP, self.localPort))

        print(f"UDP server up and listening at {self.localIP}:{self.localPort}")

        # Reset the stop_event just in case it was set from a previous run
        self.stop_event.clear()

        self.backThread = Thread(target=self.runServer)
        self.backThread.start()

    def runServer(self):
        while not self.stop_event.is_set():
            try:
                message, address = self.UDPServerSocket.recvfrom(self.bufferSize)
                decMessage = message.decode('utf-8')  # Convert bytes to string
                print(f"Received from {address}: {decMessage}")
                # Add received message to queue for processing in main thread
                self.messageQueue.append(decMessage)
            except OSError:
                # If socket is closed while blocking in recvfrom, it often raises OSError
                break
            # If you want to stop on a particular message, you could do:
            # if b"stop" in message:
            #     break

        print("Server thread stopping...")

    def stopServer(self):
        self.stop_event.set()  # Let the runServer loop exit

        # Close the socket so recvfrom returns or raises an exception
        if self.UDPServerSocket:
            try:
                self.UDPServerSocket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass  # Socket might already be closed
            self.UDPServerSocket.close()

        # Join the thread to ensure it has finished
        if self.backThread:
            self.backThread.join()
            self.backThread = None

        print("Server fully stopped.")

    def change_network(self, ipaddress):
        self.stopServer()
        self.localIP = ipaddress
        print(f"Network changed to {self.localIP}")
        self.startServer()

    def returnMessages(self):
        messages = self.messageQueue[:]  # Create a copy of the list
        self.messageQueue.clear()  # Clear the list
        return messages if messages else None