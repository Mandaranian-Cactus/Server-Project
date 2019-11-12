import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()     # Gets the initial info of the player from server.py
        # Pretty sure self.p never gets updated again

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)  # Attempts to connect to the server
            return pickle.loads(self.client.recv(2048))     # Load incoming info (Player info as an object)
        except:  # Errors such as wrong address or not available port may appear
            pass    # In which case, we pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))    # Send info of global hand (and any possible edits)
            return pickle.loads(self.client.recv(2048))     # Receive info of global (and any possible other edits)
        except socket.error as e:   # Idk, just a socket error of some sort
            print(e)
