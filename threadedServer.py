import socket
from _thread import *
import sys
import pickle
# Add the import class later when we have the correct data to send
# from PLAYER_CLASS import PLAYER
from constants import *
# from single_player.game import Player
from game import Player

# The IP is just the computer's local IP
server = SERVER_ADDRESS
port = SERVER_PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
    print("Binded to: ", server, port)
except socket.error as e:
    print(e)

# The number represents how many clients you want (it's optional)
s.listen(2)
print("Waiting for a connection. Server Started!")

# If the user is the first Player, send the other one, vice versa
# Doesn't really matter what's in here, just make sure only 2 for now
# Otherwise have to change the logic of the server
player_data = [
    "Hello server data",        # P1 data to be sent to P2
    "This from the Phone"       # Changed immediately upon connection from P2
]
current_player = 0      # The current player
players = []        # To allow for reconnections

def threaded_client(conn: socket.socket, player : int):
    '''
    Maintains constant connection to the client on a different thread to main
    If player 1 send P2 data, and then store the data in `player_data` at the
    corresponding index.

    Should run this on new threads so that it doesn't clog up main with
    an infinite loop. <-- We do this. Yay!

    Parameters:
        - conn (socket) i don't remember what this is actually, but it's something
        - player (int) This is the index of the player
    '''
    reply = ""
    conn.send(pickle.dumps(player_data[player]))
    
    while True:
        try:
            # The int is the size of the packet (how many bits/bytes(?))
            # This is the data that the client is sending to the server
            data = conn.recv(BYTE_SIZE) # BYTE DATA, INCOMPREHENSIBLE
            # If no data is recieved, disconnect 
            if not data:
                print("Disconnected!")
                '''TODO: When player disconnects/loses connection allow possible reconnection'''
                break
            else:
                if player == 1:
                    print(pickle.loads(data))
                    reply = player_data[0]
                else: 
                    reply = player_data[1]
            data = pickle.loads(data)       # NORMAL PYTHON DATA
            player_data[player] = data      # Update the stored data
            # Reply to the client
            conn.sendall(pickle.dumps(reply))

        except Exception as e:
            print("Some error occurred in server: ", e)
            break
    print("Lost connection")
    conn.close()
    return

# Continously look for a connection
while True:
    
    # addr = IP Address
    conn, addr = s.accept()
    print("Connected to: ", addr)
    # Prevent index error if more than two clients join
    if current_player in [0, 1]:
        start_new_thread(threaded_client, (conn, current_player))
    current_player += 1