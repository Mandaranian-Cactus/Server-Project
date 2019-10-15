import pygame
import random
# from layout import Layout

# Deck is used to store cards (Card class)
# Cards are accessed randomly
# We first shuffle the deck, then pop from the top
# Every drawn card must be either "hidden" or "revealed"
# If hidden, card is sent to hand
# If revealed, card is sent to the center

class Deck():

    def __init__(self):
        print("yo")
        self.deck = []
        print(self.deck)

    def add(self, card):
        self.deck.append(card)

    def randomize(self):
        random.shuffle(self.deck)

    def flip(self):
        return self.deck.pop(0)
