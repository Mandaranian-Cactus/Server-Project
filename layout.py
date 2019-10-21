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

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((W, H))
image = pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Layout.png")
image = pygame.transform.scale(image, (900, 650))
center = Layout(190, 185, 441, 253)
private_hand = Deck(605, 480, 295, 170)  # NOTE THAT THE DECK CLASS PROB ISN'T THE MOST FITTING FOR THIS (Change later)
gear_regions = []  # Locations of gear hands
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

# infinite loop
while True:

    # Draw background image
    display_surface.blit(image, (0, 0))

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
                if len(door_deck.deck) > 0:
                    card = door_deck.flip()
                    card.x, card.y = 650, 500   # Send to private hand
                    private_hand.add(card)  # Instantly adds the card into the private hand

        # For checking click on Die
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if die.within_border(x, y, 1, 1):
                die.rolling = 1  # Initiate rolling (1 = True)

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            # quit the program.
            quit()
            pygame.quit()

        for i, card in enumerate(private_hand.deck):

            # NOTE THAT BREAK STATEMENTS PREVENT OVERLAP
            # AKA, YOU CAN ONLY INTERACT WITH 1 OBJECT AT A TIME (Selection is based on it's order within list)

            # Actually do movement
            if card.move:   # Bool to see if movement is toggled on
                card.move_to(event)
                break

            # See if to start movement
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if card.within_boarder(pos):
                    card.move = True
                    break

    # Draw die
    die.draw()

    # Edits card locations
    # Begin drawing deck
    for i, card in enumerate(private_hand.deck):

        flag = False    # Flag used to record if card was at any gear regions at any time

        # Check/Edit positions of the cards
        for gear_region in gear_regions:    # Check each gear hand region
            if gear_region.within_border(card.x, card.y, card.w, card.h):
                card.location = "gear hand"
                flag = True
                break

        if not flag:
            if center.within_border(card.x, card.y, card.w, card.h):
                card.location = "center"
            elif private_hand.within_border(card.x, card.y, card.w, card.h):
                card.location = "private hand"
            else:
                card.location = ""


        # Draw image (unzoomed and default)
        card.draw_unzoom()
        card.zoom_up()


    # Redraw everything
    pygame.display.update()

    locations = []
    # print(len(private_hand.deck))
    for card in private_hand.deck:
        locations.append(card.location)

    print(locations)
