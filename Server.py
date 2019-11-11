import socket
from _thread import *
import pickle
from card import Card
import pygame
import random

# Server script will always need to be running
# Sever script needs to be run on a machine with the same wifi as the clients

class Deck():

    def __init__(self):
        self.deck = {}

    def add(self, name, card):
        self.deck.update({name:card})

    def flip(self):
        if len(self.deck) > 0:
            name, card = list(self.deck.items())[0]
            del self.deck[name]
            return name, card

server = "192.168.0.29"
port = 5555     # Often open port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:   # We have an error where a port may not be available or ip address is incorrect
    str(e)

s.listen(5)     # number of people that cn connect onto the server
print("Waiting for a connection, Server Started")   # By this part, we have gotten the server creation done


# Door deck
door_deck = Deck()
door_deck.add("Sun", Card(r"C:\Users\dannie\PycharmProjects\untitled\Images\Sun.png", 200, 200, 25, 40))
door_deck.add("Spaghetti_Jesus", Card(r"C:\Users\dannie\PycharmProjects\untitled\Images\Spaghetti_Jesus.png", 300, 200, 25, 40))
door_deck.add("FireHawk", Card(r"C:\Users\dannie\PycharmProjects\untitled\Images\FireHawk.png", 100, 200, 25, 40))
global_hand = {}    # All card registered on the board (Key is directory and value is the class)
player_cnt = 0  # Number of players present

def threaded_client(conn, player):
    global player_cnt, global_hand
    # Pickle.dumps pretty sure deconstructs the info to store an object
    conn.send(pickle.dumps([global_hand, player]))    # Sends initial info of global hand

    while True:
        try:
            data = pickle.loads(conn.recv(4048))    # Receives and reconstructs the data (Of the global hand) from network from client

            if data == "flip":  # If the client asked to flip from the door deck
                name, card = door_deck.flip()
                card.set_id(player)  # Here, we are setting up a unique id from the player
                card.x, card.y = 650, 500
                card.location = "private hand"
                conn.send(pickle.dumps([name, card]))

            elif data == "":  conn.send(pickle.dumps(global_hand))   # Sends the info of the other players (info of b to a)

            elif data[0] == "remove":
                name = data[1]
                del global_hand[name]
                conn.send(pickle.dumps("done"))

            else:   # Else, the player gives info a change of a card
                name, card_class = data
                global_hand[name] = card_class   # New data is edited over old

                conn.send(pickle.dumps(global_hand))   # Sends the info of the other players (info of b to a)

        except:     # In-case of any errors, break
            break

    print("Lost connection")
    conn.close()    # Disconnect connection
    player_cnt -= 1  # A player has left

while True:
    conn, addr = s.accept()     # Accepts a connection and ip address (In that order) from network.py
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, player_cnt))   # Begins a thread (Connects server with player and network)
    player_cnt += 1