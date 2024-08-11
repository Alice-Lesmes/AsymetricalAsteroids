import socket
# This allows for encoding as byte data
import pickle
from classes.constants import *

# courtesy of https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
print(socket.gethostbyname(socket.gethostname()))

class Network():
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER_ADDRESS
        self.port = SERVER_PORT
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        return self.p
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            # Loads byte data
            return pickle.loads(self.client.recv(BYTE_SIZE))
            
        except Exception as e:
            print("Error connecting: ", e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(BYTE_SIZE))
        except socket.error as e:
            if DEBUG:
                print("Error sending: ", e)