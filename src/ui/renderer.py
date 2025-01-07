from src.core.game_state import GameState
from src.utils import constants as c

import pygame


class Renderer:
    """
    Class to render the game state on the screen

    Attributes:
        screen (pygame.Surface): The screen to render on
    """

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.background_image: pygame.Surface = pygame.image.load(
            "assets/images/gameplay_screen.png"
        ).convert()
        self.start_screen_image: pygame.Surface = pygame.image.load(
            "assets/images/start_screen.png"
        ).convert()
        self.button_template: pygame.Surface = pygame.image.load(
            "assets/images/button.png"
        ).convert_alpha()

    def render(self, game_state: GameState) -> None:
        """
        Render the game state on the screen

        Args:
            game_state (GameState): The current game state
        """

        if game_state.current_state == c.GameStates.START:
            self._render_start_screen(game_state)
        elif game_state.current_state == c.GameStates.PLAYING:
            self._render_playing_screen(game_state)
        elif game_state.current_state == c.GameStates.PAUSED:
            self._render_pause_screen()
        elif game_state.current_state == c.GameStates.GAME_OVER_LEADERBOARD:
            self._render_game_over_leaderboard_screen(game_state)

        pygame.display.flip()

    def _render_start_screen(self, game_state: GameState) -> None:
        self.screen.blit(self.start_screen_image, (0, 0))
        self._render_start_button(game_state)
        self._render_multiplayer_toggle_button(game_state)
        self._render_sound_toggle_button(game_state)
        self._render_music_toggle_button(game_state)
        self._render_controls_info(game_state)

    def _render_start_button(self, game_state: GameState) -> None:
        button = self.button_template.copy()
        button_rect = button.get_rect()
        button_rect.center = c.START_BUTTON_POS
        button_font = pygame.font.SysFont(c.START_BUTTON_FONT, c.START_BUTTON_FONT_SIZE)
        button_surface = button_font.render(c.START_BUTTON_TEXT, True, c.START_BUTTON_TEXT_COLOR)
        text_rect = button_surface.get_rect(center=button_rect.center)
        self.screen.blit(button, button_rect)
        self.screen.blit(button_surface, text_rect)

    def _render_multiplayer_toggle_button(self, game_state: GameState) -> None:
        button = self.button_template.copy()
        button_rect = button.get_rect()
        button_rect.center = c.MULTIPLAYER_TOGGLE_BUTTON_POS
        button_font = pygame.font.SysFont(c.MULTIPLAYER_TOGGLE_BUTTON_FONT, c.MULTIPLAYER_TOGGLE_BUTTON_FONT_SIZE)
        if game_state.multiplayer:
            button_surface = button_font.render(c.MULTIPLAYER_TOGGLE_BUTTON_TEXT_ON, True, c.MULTIPLAYER_TOGGLE_BUTTON_TEXT_COLOR)
        else:
            button_surface = button_font.render(c.MULTIPLAYER_TOGGLE_BUTTON_TEXT_OFF, True, c.MULTIPLAYER_TOGGLE_BUTTON_TEXT_COLOR)
        text_rect = button_surface.get_rect(center=button_rect.center)
        self.screen.blit(button, button_rect)
        self.screen.blit(button_surface, text_rect)

    def _render_sound_toggle_button(self, game_state: GameState) -> None:
        button = self.button_template.copy()
        button_rect = button.get_rect()
        button_rect.center = c.SOUND_TOGGLE_BUTTON_POS
        button_font = pygame.font.SysFont(c.SOUND_TOGGLE_BUTTON_FONT, c.SOUND_TOGGLE_BUTTON_FONT_SIZE)
        if not game_state.sound_manager.sound_muted:
            button_surface = button_font.render(c.SOUND_TOGGLE_BUTTON_TEXT_ON, True, c.SOUND_TOGGLE_BUTTON_TEXT_COLOR)
        else:
            button_surface = button_font.render(c.SOUND_TOGGLE_BUTTON_TEXT_OFF, True, c.SOUND_TOGGLE_BUTTON_TEXT_COLOR)
        text_rect = button_surface.get_rect(center=button_rect.center)
        self.screen.blit(button, button_rect)
        self.screen.blit(button_surface, text_rect)

    def _render_music_toggle_button(self, game_state: GameState) -> None:
        button = self.button_template.copy()
        button_rect = button.get_rect()
        button_rect.center = c.MUSIC_TOGGLE_BUTTON_POS
        button_font = pygame.font.SysFont(c.MUSIC_TOGGLE_BUTTON_FONT, c.MUSIC_TOGGLE_BUTTON_FONT_SIZE)
        if not game_state.sound_manager.music_muted:
            button_surface = button_font.render(c.MUSIC_TOGGLE_BUTTON_TEXT_ON, True, c.MUSIC_TOGGLE_BUTTON_TEXT_COLOR)
        else:
            button_surface = button_font.render(c.MUSIC_TOGGLE_BUTTON_TEXT_OFF, True, c.MUSIC_TOGGLE_BUTTON_TEXT_COLOR)
        text_rect = button_surface.get_rect(center=button_rect.center)
        self.screen.blit(button, button_rect)
        self.screen.blit(button_surface, text_rect)

    def _render_controls_info(self, game_state: GameState) -> None:
        font = pygame.font.SysFont(c.CONTROLS_INFO_FONT, c.CONTROLS_INFO_FONT_SIZE)

        instruction_surface = font.render(c.CONTROLS_INFO_TEXT, True, c.CONTROLS_INFO_TEXT_COLOR)
        instruction_rect = instruction_surface.get_rect(center=c.CONTROLS_INFO_POS)
        self.screen.blit(instruction_surface, instruction_rect)

    def _render_playing_screen(self, game_state: GameState) -> None:
        self.screen.blit(self.background_image, (0, 0))
        game_state.all_sprites.draw(self.screen)
        game_state.bonus_star.particle_system.update()
        game_state.bonus_star.particle_system.draw(self.screen)

    def _render_pause_screen(self) -> None:
        self.screen.blit(self.background_image, (0, 0))

    def _render_game_over_leaderboard_screen(self, game_state: GameState) -> None:
        self.screen.blit(self.background_image, (0, 0))
