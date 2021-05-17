import pygame


class Ship:
    """A class designed to manage a spacecraft."""

    def __init__(self, ai_game):
        """Initialization of the spacecraft and its initial position."""

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Loading a spacecraft image and retrieving its rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Each new spacecraft appears at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Options indicating the movement of the spacecraft
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Updating the position of a spacecraft based on an option indicating its movement."""
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1

    def blitme(self):
        """Display the spacecraft in its current position."""
        self.screen.blit(self.image, self.rect)
