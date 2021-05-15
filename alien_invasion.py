import sys

import pygame

from settings import Settings

class AlienInvasion:
    """This is a general class designed to manage resources and how the game works."""

    def __init__(self):
        """Initialization of the game and creation of its resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")


    def run_game(self):
        """Starting the main game loop"""
        while True:
            #Waiting for a key or mouse click
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #Refresh the screen during each iteration of the loop.
            self.screen.fill(self.settings.bg_color)

            #Display last modified screen
            pygame.display.flip()

if __name__ == '__main__':
    #Creating a copy of the game and launching it
    ai = AlienInvasion()
    ai.run_game()