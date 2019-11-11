import pygame
# from dice import Dice
from card import Card
import time
import random
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
        super().__init__(x, y, w, h)    # Does init from Layout class
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

class Dice(Layout):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.num = -1
        self.rolls = []
        self.rolling = 0  # False
        self.rolls.append(pygame.transform.scale(pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Dice\1.png"), (self.w, self.h)))
        self.rolls.append(pygame.transform.scale(pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Dice\2.png"), (self.w, self.h)))
        self.rolls.append(pygame.transform.scale(pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Dice\3.png"), (self.w, self.h)))
        self.rolls.append(pygame.transform.scale(pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Dice\4.png"), (self.w, self.h)))
        self.rolls.append(pygame.transform.scale(pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Dice\5.png"), (self.w, self.h)))
        self.rolls.append(pygame.transform.scale(pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Dice\6.png"), (self.w, self.h)))

    def draw(self):
        display_surface.blit(self.rolls[self.num], (self.x, self.y))

    def roll(self):
        self.num = random.randrange(0, 6)

# assigning values to X and Y variable
W = 900
H = 650

# Create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((W, H))
image = pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Layout.png")
image = pygame.transform.scale(image, (900, 650))
center = Layout(190, 185, 441, 253)
private_hand = Layout(605, 480, 295, 170)  # NOTE THAT THE DECK CLASS PROB ISN'T THE MOST FITTING FOR THIS (Change later)
global_hand = []    # All card registered on the board

gear_regions = []  # Locations of gear hands (Gear regions do not actually store the cards in them)
gear_regions.append(Layout(188, 517, 338, 101))
gear_regions.append(Layout(707, 80, 117, 316))
gear_regions.append(Layout(212, 18, 349, 121))
gear_regions.append(Layout(13, 157, 89, 317))

# Add to Deck
door_deck = Deck(208, 209, 49, 89)
door_deck.add(Card(r"C:\Users\dannie\PycharmProjects\untitled\Images\Sun.png", 200, 200, 25, 40))
door_deck.add(Card(r"C:\Users\dannie\PycharmProjects\untitled\Images\Spaghetti_Jesus.png", 300, 200, 25, 40))
door_deck.add(Card(r"C:\Users\dannie\PycharmProjects\untitled\Images\FireHawk.png", 100, 200, 25, 40))
door_deck.randomize()

# Die
die = Dice(280, 210, 50, 50)

def update():
    # Check to see if Die is being rolled
    if 0 < die.rolling <= 50:   # Basically 50-micro rolls
        die.roll()
        die.rolling += 1
    else:   # Reset die to be not rolling (0 = False)
        die.rolling = 0

    for event in pygame.event.get():
        # For checking clicks on decks (DOOR DECK ONLY RN)
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if door_deck.within_border(x, y, 1, 1):
                if len(door_deck.deck) > 0: # Makes sure deck is not empty
                    card = door_deck.flip()
                    card.x, card.y = 650, 500   # Send to private hand for positions
                    card.location = "private hand"  # Instantly marks the location as being in the private hand
                    card.load()  # Loading the card basically means loading the card's image and image features
                    print(card.location)
                    global_hand.append(card)    # Card is taken away from the deck and added into the board

        # For checking click on Die
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if die.within_border(x, y, 1, 1):
                die.rolling = 1  # Initiate rolling (1 = True)

        # For exiting the game
        if event.type == pygame.QUIT:
            # quit the program.
            quit()
            pygame.quit()

        # Drag and drop interaction
        for i, card in enumerate(global_hand):

            # NOTE THAT BREAK STATEMENTS PREVENT OVERLAP
            # AKA, YOU CAN ONLY INTERACT WITH 1 OBJECT AT A TIME (Selection is based on it's order within list)
            # Checks activation and movements and also performs movement if necessary
            if card.move_to(event): break

    # Edits card locations
    # Begin drawing deck
    for card in global_hand:

        flag = False    # Flag used to record if card was found at any gear regions at any time

        # Check/Edit location of the cards (Stored into class variable)
        for gear_region in gear_regions:    # Check each gear hand region
            if gear_region.within_border(card.x, card.y, card.w, card.h):
                card.location = "gear hand"
                flag = True
                break

        if not flag:    # Card not in any gear hand regions
            if center.within_border(card.x, card.y, card.w, card.h):
                card.location = "center"
            elif private_hand.within_border(card.x, card.y, card.w, card.h):
                card.location = "private hand"
            else:
                card.location = ""


def draw():

    # Draw background image
    display_surface.blit(image, (0, 0))

    # Draw die
    die.draw()

    # Draw image (unzoomed and default)
    for card in global_hand:
        card.draw_unzoom()
        card.zoom_up()


# infinite loop
def main():
    while True:
        update()
        draw()

        # Redraw everything
        pygame.display.update()

        locations = []
        for card in global_hand:
            locations.append(card.location)

        print(locations)
main()