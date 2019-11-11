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

class Layout:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def within_border(self, x, y, w, h):

        if self.x <= x and x + w <= self.x + self.w:
            if self.y <= y and y + h <= self.y + self.h:
                return True

        return False


class Deck(Layout):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)    # Does init from Layout class
        self.deck = []
        print(self.deck)

    def add(self, card):
        self.deck.append(card)

    def randomize(self):
        random.shuffle(self.deck)

    def flip(self):
        return self.deck.pop(0)
