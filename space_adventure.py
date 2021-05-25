import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
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

        # Create an instance that stores game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Creating a Game button
        self.play_button = Button(self, 0, "Game")

    def run_game(self):
        """Starting the main game loop"""
        while True:
            self._check_events()

            if self.stats.game_active:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def check_play_button(self, mouse_pos):
        """Starting a new game by pressing the Game button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not  self.stats.game_active:
            # Reset the game stats.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()

            # Empty aliens and bullets lists.
            self.aliens.empty()
            self.bullets.empty()

            # Create enemies and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse cursor
            pygame.mouse.set_visible(False)

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
        # Removing projectiles that are outside the screen.
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        # Checking if the projectile hit the enemy, if yes, we remove the projectile and the enemy from the screen.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()

        if not self.aliens:
            # Getting rid of existing bullets and creating a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_aliens(self):
        """Checking for enemies near the edge, then updating the location of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Collision detection between enemy and player
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Checking if the enemy has reached the bottom of the screen
        self._check_aliens_bottom()

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

    def _check_fleet_edges(self):
        """Adequate reaction when the enemy reaches the edge of the screen."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Moving the entire fleet down and changing the direction in which it moves."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Reaction to enemy hitting the ship"""
        if self.stats.ships_left > 0:
            # Reduction in the value of owned ships
            self.stats.ships_left -= 1

            # Removing the contents of the aliens and bullets lists.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Checking if the enemy has reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # The same as when a ship collides with an enemy
                self._ship_hit()
                break

    def _update_screen(self):
        # Refresh the screen during each iteration of the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Display of scoring information
        self.sb.show_score()

        # Displaying the button when the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Display last modified screen
        pygame.display.flip()


if __name__ == '__main__':
    # Creating a copy of the game and launching it
    ai = SpaceAdventure()
    ai.run_game()
