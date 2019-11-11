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
        self.location = ""
        self.move = False   # Boolean to check if moving the image is toggled
        self.image = image

    def set_id(self, id):
        self.id = id

    def draw_unzoom(self, loaded):  # Actually draw the object
        display_surface.blit(pygame.transform.scale(loaded, (self.w, self.h)), (self.x, self.y))

    def draw_zoom(self, loaded):  # Display Zoomed up version
        w, h = pygame.display.get_surface().get_size()
        display_surface.blit(pygame.transform.scale(loaded, (300, 400)), (w / 2 - 300 / 2, h / 2 - 400 / 2))

    def within_boarder(self, pos):  # Border check for seeing if mouse click is within boarder
        mx, my = pos
        if self.x < mx < self.x + self.w:
            if self.y < my < self.y + self.h:
                return True  # Clicking on it

        return False  # Not clicking it

    def move_to(self, event):  # Checks to see if movement is possible and also if to execute movement of a card
        # Update coords

        # See if to start movement
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.within_boarder(pos):
                self.move = True

        # See if to end movement (Only if movement was already activated)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.move = False  # Basically stops movement and resets card to be still
            return False    # Means that the movement is cut

        # Actually edit coords and do movement
        if self.move:
            pos = pygame.mouse.get_pos()
            self.x = pos[0] - self.w/2
            self.y = pos[1] - self.h/2
            return True     # Means that the movement continues

    # First checks to see if within boarder
    # Then checks to see if "e" is held down
    # If both satisfied, return True (Player is asking for a zoom)
    def zoom_up(self, loaded):  # Zoom up on image (Check to see if "e" is pressed as a toggle)
        pos = pygame.mouse.get_pos()
        if self.within_boarder(pos):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:  # "e" key as the toggle is being pressed
                self.draw_zoom(loaded)    # Draw zoomed up version