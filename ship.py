import pygame

class Ship:
    """A class designed to manage a spacecraft."""

    def __init__(self, ai_game):
        """Initialization of the spacecraft and its initial position."""

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        """Loading a spacecraft image and retrieving its rectangle"""
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        """Each new spacecraft appears at the bottom of the screen"""
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Display the spacecraft in its current position."""
        self.screen.blit(self.image, self.rect)