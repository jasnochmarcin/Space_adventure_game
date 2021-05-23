import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class SpaceAdventure:
    """This is a general class designed to manage resources and how the game works."""

    def __init__(self):
        """Initialization of the game and creation of its resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Space Adventure")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Starting the main game loop"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Response to keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Response to key press"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Response to key release"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_q:
            sys.exit()

    def _fire_bullet(self):
        """Creating a new projectile and adding it to a projectile group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Updating the position of projectiles and removing projectiles that are outside the scree"""
        # Updating the position of projectiles
        self.bullets.update()

        # Removing projectiles that are outside the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_aliens(self):
        """Updating the position of all enemies"""
        self.aliens.update()

    def _create_fleet(self):
        """Creating a full fleet of enemies"""
        # Creating an enemy and determining the number of enemies that will fit in a row
        # The distance between each enemy is equal to the width of one enemy
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avaiable_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avaiable_space_x // (2 * alien_width)

        # Determine how many rows of enemies will fit on the screen
        ship_height = self.ship.rect.height
        avaiable_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = avaiable_space_y // (2 * alien_height)

        # Creating a full fleet of enemies
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Creating an enemy and placing it in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        # Refresh the screen during each iteration of the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Display last modified screen
        pygame.display.flip()


if __name__ == '__main__':
    # Creating a copy of the game and launching it
    ai = SpaceAdventure()
    ai.run_game()
