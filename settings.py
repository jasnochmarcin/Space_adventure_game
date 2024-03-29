class Settings:
    """A class dedicated to store all game settings"""

    def __init__(self):
        """Initialize game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Enemies settings
        self.fleet_drop_speed = 10

        # Easy change of game speed
        self.speedup_scale = 1.1

        # Easily change the number of points awarded for killing an enemy
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change during the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 1

        # A value in fleet_direction = 1 indicates right, while -1 indicates left.
        self.fleet_direction = 1

        # Scores
        self.alien_points = 50

    def increase_speed(self):
        """Changing the speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
