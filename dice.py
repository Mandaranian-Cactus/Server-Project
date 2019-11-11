import random
import pygame
from layout import Layout
W = 0
H = 0
display_surface = pygame.display.set_mode((W, H))

class Dice(Layout):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.num = -1
        self.rolls = []
        self.rolling = 0    # False
        self.rolls.append(pygame.transform.scale(pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Dice\1.png"), (self.w, self.h)))
        self.rolls.append(pygame.transform.scale(pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Dice\2.png"), (self.w, self.h)))
        self.rolls.append(pygame.transform.scale(pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Dice\3.png"), (self.w, self.h)))
        self.rolls.append(pygame.transform.scale(pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Dice\4.png"), (self.w, self.h)))
        self.rolls.append(pygame.transform.scale(pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Dice\5.png"), (self.w, self.h)))
        self.rolls.append(pygame.transform.scale(pygame.image.load(r"C:\Users\dannie\PycharmProjects\untitled\Images\Dice\6.png"), (self.w, self.h)))

    def draw(self):
        display_surface.blit(self.rolls[self.num], (self.x, self.y))

    def roll(self):
        num = random.randrange(0, 6)
        self.num = num
