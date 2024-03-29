class GameStats:
    """Monitoring in-game statistics."""

    def __init__(self, ai_game):
        """Initialization of statistical data."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Space Adventur in an active state.
        self.game_active = False

        # The best score should be retained
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that may change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
