import pygame


class Ship:
    """A class designed to manage a spacecraft."""

    def __init__(self, ai_game):
        """Initialization of the spacecraft and its initial position."""

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Loading a spacecraft image and retrieving its rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Each new spacecraft appears at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # The ship position is stored as a float
        self.x = float(self.rect.x)

        # Options indicating the movement of the spacecraft
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Updating the position of a spacecraft based on an option indicating its movement."""
        # Updating the x-coordinate value of a ship, not its rectangle
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Updating a rect object based on the value of self.x
        self.rect.x = self.x

    def blitme(self):
        """Display the spacecraft in its current position."""
        self.screen.blit(self.image, self.rect)
