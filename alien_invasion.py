import sys

import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """This is a general class designed to manage resources and how the game works."""

    def __init__(self):
        """Initialization of the game and creation of its resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

    def run_game(self):
        """Starting the main game loop"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        # Waiting for a key or mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _update_screen(self):
        # Refresh the screen during each iteration of the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # Display last modified screen
        pygame.display.flip()


if __name__ == '__main__':
    # Creating a copy of the game and launching it
    ai = AlienInvasion()
    ai.run_game()
