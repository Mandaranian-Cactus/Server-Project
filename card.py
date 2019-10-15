import pygame
W = 0
H = 0
display_surface = pygame.display.set_mode((W, H))

class Card:

    def __init__(self, image, x, y, w, h):  # Initialize basic info
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.move = False   # Boolean to check if moving the image is toggled
        self.zoom_bool = False   # Whether or not tro draw the zoomed up version
        self.image = pygame.image.load(image)
        self.unzoomed = pygame.transform.scale(self.image, (self.w, self.h))
        self.zoomed = pygame.transform.scale(self.image, (300, 400))

    def draw_unzoom(self):  # Actually draw the object
        display_surface.blit(self.unzoomed, (self.x, self.y))

    def draw_zoom(self):
        w, h = pygame.display.get_surface().get_size()
        display_surface.blit(self.zoomed, (w / 2 - 300 / 2, h / 2 - 400 / 2))

    def within_boarder(self, pos):  # Border check for seeing if mouse click is within boarder
        mx, my = pos
        if self.x < mx < self.x + self.w:
            if self.y < my < self.y + self.h:
                return True  # Clicking on it

        return False  # Not clicking it

    def move_to(self, event):  # Transition from "within_boarder" where we now move the image
        # Update coords
        pos = pygame.mouse.get_pos()
        self.x = pos[0] - self.w/2
        self.y = pos[1] - self.h/2

        if event.type == pygame.MOUSEBUTTONUP: self.move = False


    # First checks to see if within boarder
    # Then checks to see if "e" is held down
    # If both satisfied, return True (Player is asking for a zoom)
    def zoom_up(self):  # Zoom up on image (Check to see if "e" is pressed as a toggle)
        pos = pygame.mouse.get_pos()
        if self.within_boarder(pos):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                return True