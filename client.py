import pygame
from card import Card
import time
import random
from network import Network
import time

# from deck import Deck


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
        super().__init__(x, y, w, h)  # Does init from Layout class
        self.deck = []

    def add(self, card):
        self.deck.append(card)

    def randomize(self):
        random.shuffle(self.deck)

    def flip(self):
        return self.deck.pop(0)


class Hand(Layout):
    def __init__(self, x, y, w, h):
        self.hand = []
        super().__init__(x, y, w, h)

    def add(self, card):
        self.hand.append(card)



# assigning values to X and Y variable
W = 900
H = 650

# Create the display surface object
display_surface = pygame.display.set_mode((W, H))
image = pygame.image.load(r"/home/robuntu/Thomas/Server-Project/Layout.png")
image = pygame.transform.scale(image, (900, 650))
private_hand = Layout(605, 480, 295, 170)  # NOTE THAT THE DECK CLASS PROB ISN'T THE MOST FITTING FOR THIS (Change later)

# Trash can
trash_can = Layout(0, 555, 73, 95)

# Door Deck
door_deck = Layout(208, 209, 49, 89)



# Private hand
personal_hand = {}

# Random needed stuff
run = True
# Network is essentially the conversation
n = Network()  # Network is set up and begins an infinite loop through threading in server.py
global_hand, player_num = n.getP()  # # Get the initial position (From network.py which got from server.py
clock = pygame.time.Clock()


def update():
    global n, global_hand

    # Edits card locations
    for name in global_hand:
        card = global_hand[name]  # May be bad code

        if private_hand.within_border(card.x, card.y, card.w, card.h):
            if card.id == player_num:
                card.location = "private hand"
                personal_hand.update({name: card})
                del global_hand[name]
                n.send(["remove", name])
            break

        if trash_can.within_border(card.x, card.y, card.w, card.h):
            n.send(["remove", name])
            del global_hand[name] # For duplication glitches (sorta a glitch)
            break

    for name in personal_hand:
        card = personal_hand[name]  # May be bad code

        if not private_hand.within_border(card.x, card.y, card.w, card.h):
            card.location = "center"
            del personal_hand[name]
            n.send([name, card])  # Send Card going into personal hand (Newly changed info)
            break

    for event in pygame.event.get():
        # For checking clicks on decks (DOOR DECK ONLY RN)
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if door_deck.within_border(x, y, 1, 1):
                name, card = n.send("flip")
                personal_hand.update({name: card})

        # For exiting the game
        elif event.type == pygame.QUIT:
            # quit the program.
            quit()
            pygame.quit()

        # Drag and drop interaction
        for card in global_hand:
            # NOTE THAT BREAK STATEMENTS PREVENT OVERLAP
            # AKA, YOU CAN ONLY INTERACT WITH 1 OBJECT AT A TIME (Selection is based on it's order within list)
            # Checks activation and movements and also performs movement if necessary
            if global_hand[card].move_to(event):
                n.send([card, global_hand[card]])
                break

            n.send([card, global_hand[card]])

        for card in personal_hand:

            # NOTE THAT BREAK STATEMENTS PREVENT OVERLAP
            # AKA, YOU CAN ONLY INTERACT WITH 1 OBJECT AT A TIME (Selection is based on it's order within list)
            # Checks activation and movements and also performs movement if necessary
            if personal_hand[card].move_to(event):
                break


def draw():
    # Draw background image
    display_surface.blit(image, (0, 0))

    # Draw image (unzoomed and default)
    for directory in global_hand:
        card = global_hand[directory]
        loaded = pygame.image.load(card.image)
        global_hand[directory].draw_unzoom(loaded)
        global_hand[directory].zoom_up(loaded)

    for directory in personal_hand:
        card = personal_hand[directory]
        loaded = pygame.image.load(card.image)
        personal_hand[directory].draw_unzoom(loaded)
        personal_hand[directory].zoom_up(loaded)

# infinite loop
def main():
    global global_hand

    while True:
        clock.tick(60)  # Set refresh rate???????
        update()
        draw()
        players = n.send('')      # send info of p1 then get info of p2
        global_hand = players

        # Redraw everything
        pygame.display.update()



main()
