from src.core.game_state import GameState
from src.utils.screenshot import ScreenshotManager

import pygame


class EventHandler:
    """
    Class to handle all the events in the game

    Args:
        game_state (GameState): The current game state

    Attributes:
        game_state (GameState): The current game state
        screenshot_manager (ScreenshotManager): The screenshot manager
                to take screenshots

    """

    def __init__(self, game_state: GameState) -> None:
        self.game_state = game_state
        self.screenshot_manager = ScreenshotManager()

    def handle_events(self) -> bool:
        """
        Handle all the events in the game

        Returns:
            bool: True if the game should continue, False if the game should end
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                return self._handle_keyboard(event)
        return True


    def _handle_keyboard(self, event) -> bool:
        """
        Handle the keyboard events

        Args:
            event (pygame.event.Event): The keyboard event

        Returns:
            bool: True if the game should continue, False if the game should end
        """
        if event.key == pygame.K_UP:
            self.game_state.cloud_player2.move("up")
        elif event.key == pygame.K_DOWN:
            self.game_state.cloud_player2.move("down")
        elif event.key == pygame.K_w:
            self.game_state.cloud_player1.move("up")
        elif event.key == pygame.K_s:
            self.game_state.cloud_player1.move("down")
        return True
