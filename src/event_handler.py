from src.core.game_state import GameState
from src.ui.renderer import Renderer
from src.utils import constants as c
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
            elif (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):
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

    def _handle_start_screen_click(self, mouse_pos):
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

    def _handle_paused_screen_click(self, mouse_pos):
        if self.renderer.sound_button.is_clicked(mouse_pos):
            self.game_state.sound_manager.toggle_sound()
            self.game_state.sound_manager.play_sound("mouse-click")

        elif self.renderer.music_button.is_clicked(mouse_pos):
            self.game_state.sound_manager.toggle_music()
            self.game_state.sound_manager.play_sound("mouse-click")

    def _handle_keydown(self, event: pygame.event.Event) -> bool:
        if event.key == pygame.K_ESCAPE:
            if self.game_state.current_state == c.GameStates.START:
                return False
            elif self.game_state.current_state == c.GameStates.PLAYING:
                self.game_state.set_state(c.GameStates.PAUSED)
            elif self.game_state.current_state == c.GameStates.PAUSED:
                self.game_state.set_state(c.GameStates.GAME_OVER_LEADERBOARD)
            elif self.game_state.current_state == c.GameStates.GAME_OVER_LEADERBOARD:
                self.game_state.set_state(c.GameStates.START)
                self.game_state.reset()

        elif event.key == pygame.K_SPACE:
            if self.game_state.current_state == c.GameStates.PLAYING:
                self.game_state.set_state(c.GameStates.PAUSED)
            elif self.game_state.current_state == c.GameStates.PAUSED:
                self.game_state.set_state(c.GameStates.PLAYING)

        return True
