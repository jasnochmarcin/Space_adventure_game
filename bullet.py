import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class designed to manage the projectiles fired by a ship."""

    def __init__(self, ai_game):
        """Create a projectile object at the current ship position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # Create a projectile object at point (0, 0) and then define the appropriate position for it
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_width)
        self.rect.midtop = ai_game.ship.rect.midtop

        # The bullet position is defined by a floating point value
        self.y = float(self.rect.y)

    def update(self):
        """Moving a projectile across the screen"""
        # Updating the projectile position
        self.y -= self.settings.bullet_speed
        # Updating the position of the projectile rectangle
        self.rect.y = self.y

    def draw_bullet(self):
        """Displaying the projectile on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)