from src.core.game_state import GameState
from src.ui.renderer import Renderer
from src.utils import constants as c
from src.utils.helpers import save_current_score
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

    def __init__(self, game_state: GameState, renderer: Renderer) -> None:
        self.game_state = game_state
        self.screenshot_manager = ScreenshotManager()
        self.renderer = renderer

    def handle_events(self) -> bool:
        """
        Handle all the events in the game

        Returns:
            bool: True if the game should continue, False if the game should end
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.game_state.current_state == c.GameStates.START:
                    self._handle_start_screen_click(mouse_pos)
                elif self.game_state.current_state == c.GameStates.PAUSED:
                    self._handle_paused_screen_click(mouse_pos)
            elif event.type == c.BONUS_SPAWN_EVENT:
                self.game_state.bonus_star.spawn()
            elif event.type == c.BONUS_DE_SPAWN_EVENT:
                self.game_state.bonus_star.despawn()
            elif event.type == pygame.KEYDOWN:
                return self._handle_keydown(event)
        return True

    def _handle_start_screen_click(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle the click events on the start screen

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse click
        """
        if self.renderer.start_button.is_clicked(mouse_pos):
            self.game_state.set_state(c.GameStates.PLAYING)
            self.game_state.sound_manager.play_sound("mouse-click")

        elif self.renderer.multiplayer_button.is_clicked(mouse_pos):
            self.game_state.toggle_multiplayer()
            self.game_state.sound_manager.play_sound("mouse-click")

        elif self.renderer.sound_button.is_clicked(mouse_pos):
            self.game_state.sound_manager.toggle_sound()
            self.game_state.sound_manager.play_sound("mouse-click")

        elif self.renderer.music_button.is_clicked(mouse_pos):
            self.game_state.sound_manager.toggle_music()
            self.game_state.sound_manager.play_sound("mouse-click")

    def _handle_paused_screen_click(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle the click events on the paused screen

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse click
        """
        if self.renderer.sound_button.is_clicked(mouse_pos):
            self.game_state.sound_manager.toggle_sound()
            self.game_state.sound_manager.play_sound("mouse-click")

        elif self.renderer.music_button.is_clicked(mouse_pos):
            self.game_state.sound_manager.toggle_music()
            self.game_state.sound_manager.play_sound("mouse-click")

    def _handle_keydown(self, event: pygame.event.Event) -> bool:
        """
        Handle the keydown events

        Args:
            event (pygame.event.Event): The keydown event
        """
        if event.key == pygame.K_ESCAPE:
            return self._handle_escape_key()

        elif event.key == pygame.K_SPACE:
            return self._handle_space_key()

        elif event.key == pygame.K_c:
            self.screenshot_manager.capture_game_state(
                self.renderer.screen, self.game_state
            )

        return True

    def _handle_escape_key(self) -> bool:
        """
        Handle the escape key press

        Returns:
            bool: True if the game should continue, False if the game should end
        """
        if self.game_state.current_state == c.GameStates.START:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return True
        elif self.game_state.current_state == c.GameStates.PLAYING:
            self.game_state.set_state(c.GameStates.PAUSED)
        elif self.game_state.current_state == c.GameStates.PAUSED:
            self.game_state.set_state(c.GameStates.GAME_OVER_LEADERBOARD)
            scores = [self.game_state.player1_score]
            if self.game_state.multiplayer:
                scores.append(self.game_state.player2_score)
            save_current_score(scores)
        elif self.game_state.current_state == c.GameStates.GAME_OVER_LEADERBOARD:
            self.game_state.set_state(c.GameStates.START)
            self.game_state.reset()

        return True

    def _handle_space_key(self) -> bool:
        """
        Handle the space key press

        Returns:
            bool: True if the game should continue, False if the game should
        """
        if self.game_state.current_state == c.GameStates.PLAYING:
            self.game_state.set_state(c.GameStates.PAUSED)
        elif self.game_state.current_state == c.GameStates.PAUSED:
            self.game_state.set_state(c.GameStates.PLAYING)

        return True
