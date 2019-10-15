import pygame
from card import Card
import random
from deck import Deck

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

# define the RGB value
# for white colour
white = (255, 255, 255)

# assigning values to X and Y variable
W = 900
H = 650

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((W, H))
image = pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Layout.png")
image = pygame.transform.scale(image, (900, 650))
center = Layout(190, 185, 441, 253)
private_hand = Deck(605, 480, 295, 170)
gear_hands = []
locations = ["" for i in range(40)]
gear_hands.append(Layout(188, 517, 338, 101))
gear_hands.append(Layout(707, 80, 117, 316))
gear_hands.append(Layout(212, 18, 349, 121))
gear_hands.append(Layout(13, 157, 89, 317))

# Add to Deck
deck = Deck(208, 209, 49, 89)
deck.add(Card(r"C:\Users\dannie\PycharmProjects\untitled\Images\Sun.png", 200, 200, 25, 40))
deck.add(Card(r"C:\Users\dannie\PycharmProjects\untitled\Images\Spaghetti_Jesus.png", 300, 200, 25, 40))
deck.add(Card(r"C:\Users\dannie\PycharmProjects\untitled\Images\FireHawk.png", 100, 200, 25, 40))
deck.randomize()

# infinite loop
while True:

    # Draw background image
    display_surface.blit(image, (0, 0))

    for event in pygame.event.get():
    # FIXXXXX
        # For checking clicks on decks
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if deck.within_border(x, y, 1, 1):
                if len(deck.deck) > 0:
                    card = deck.flip()
                    card.x, card.y = 650, 500   # Send to hand
                    private_hand.add(card)

    # FIXXXXXX

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            # quit the program.
            quit()

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     print(pos)

        for i, card in enumerate(private_hand.deck):

            # NOTE THAT BREAK STATEMENTS PREVENT OVERLAP
            # AKA, YOU CAN ONLY INTERACT WITH 1 OBJECT AT A TIME (Selection is based on it's order within list)

            # Actually do movement
            if card.move:
                card.move_to(event)
                break

            # See if to start movement
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if card.within_boarder(pos):
                    card.move = True
                    break

            # No break statement needed here
            # See if to zoom up
            if card.zoom_up(): card.zoom_bool = True    # Zoom up
            else: card.zoom_bool = False    # Done zooming up


    for i, card in enumerate(private_hand.deck):

        # Check/Edit positions of the cards
        for gear_hand in gear_hands:
            flag = False    # Flag to see if card is at a gear hand or not (Later flag gonna be removed)
            if gear_hand.within_border(card.x, card.y, card.w, card.h):
                locations[i] = "gear hand"
                flag = True
                break
            elif center.within_border(card.x, card.y, card.w, card.h):
                locations[i] = "center"
                flag = True
                break
            elif private_hand.within_border(card.x, card.y, card.w, card.h):
                locations[i] = "private hand"
                flag = True
                break

        if not flag: locations[i] = ""


        # Draw image
        card.draw_unzoom()

    for i, card in enumerate(private_hand.deck):  # For overlap issues
        if card.zoom_bool: card.draw_zoom()  # Draw zoomed up version

    # Redraw everything
    pygame.display.update()
    # print(locations)

