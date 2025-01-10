from datetime import datetime
import os

from src.utils import constants as c

import pygame


class ScreenshotManager:
    def __init__(self, base_path="assets/screenshots"):
        """Initialize the screenshot manager with a base directory path."""
        self.base_path = base_path
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Create the screenshots directory if it doesn't exist."""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def _capture(self, screen: pygame.Surface, name: str):
        """
        Capture a screenshot of the current game state.

        Args:
            screen: The pygame surface to capture
            name: Name for the screenshot (e.g., 'start_screen', 'game_in_progress')
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.base_path, filename)

        pygame.image.save(screen, filepath)
        print(f"Screenshot saved: {filepath}")

    def capture_game_state(self, screen: pygame.Surface, game_state):
        """
        Intelligent capture based on current game state.

        Args:
            screen: The pygame surface to capture
            game_state: Current GameState instance
        """
        if game_state.current_state == c.GameStates.START:
            self._capture(screen, "start_screen")
        elif game_state.current_state == c.GameStates.GAME_OVER_LEADERBOARD:
            self._capture(screen, "game_over")
        elif game_state.current_state == c.GameStates.PAUSED:
            self._capture(screen, "paused")

        else:
            self._capture(screen, "game_in_progress")
