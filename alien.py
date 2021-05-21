import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class representing a single enemy"""

    def __init__(self, ai_game):
        """Initialize the enemy and define its initial position."""
        super().__init__()
        self.screen = ai_game.screen

        # Load the opponent's image and define its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Placing a new enemy near the top left corner of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Storing the exact horizontal location of the opponent.
        self.x = float(self.rect.x)