from src.core.game_state import GameState
from src.ui.button import Button
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

        # Създаваме бутоните
        self.start_button = Button(
            self.button_template.copy(),
            c.START_BUTTON_POS,
            c.START_BUTTON_TEXT,
            c.START_BUTTON_FONT,
            c.START_BUTTON_FONT_SIZE,
            c.START_BUTTON_TEXT_COLOR
        )

        self.multiplayer_button = Button(
            self.button_template.copy(),
            c.MULTIPLAYER_TOGGLE_BUTTON_POS,
            c.MULTIPLAYER_TOGGLE_BUTTON_TEXT_OFF,
            c.MULTIPLAYER_TOGGLE_BUTTON_FONT,
            c.MULTIPLAYER_TOGGLE_BUTTON_FONT_SIZE,
            c.MULTIPLAYER_TOGGLE_BUTTON_TEXT_COLOR
        )

        self.sound_button = Button(
            self.button_template.copy(),
            c.SOUND_TOGGLE_BUTTON_POS,
            c.SOUND_TOGGLE_BUTTON_TEXT_ON,
            c.SOUND_TOGGLE_BUTTON_FONT,
            c.SOUND_TOGGLE_BUTTON_FONT_SIZE,
            c.SOUND_TOGGLE_BUTTON_TEXT_COLOR
        )

        self.music_button = Button(
            self.button_template.copy(),
            c.MUSIC_TOGGLE_BUTTON_POS,
            c.MUSIC_TOGGLE_BUTTON_TEXT_ON,
            c.MUSIC_TOGGLE_BUTTON_FONT,
            c.MUSIC_TOGGLE_BUTTON_FONT_SIZE,
            c.MUSIC_TOGGLE_BUTTON_TEXT_COLOR
        )

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
        self._render_start_button()
        self._render_multiplayer_toggle_button(game_state)
        self._render_sound_toggle_button(game_state)
        self._render_music_toggle_button(game_state)
        self._render_controls_info()

    def _render_start_button(self) -> None:
        self.start_button.draw(self.screen)

    def _render_multiplayer_toggle_button(self, game_state: GameState) -> None:
        text = c.MULTIPLAYER_TOGGLE_BUTTON_TEXT_ON if game_state.multiplayer else c.MULTIPLAYER_TOGGLE_BUTTON_TEXT_OFF
        self.multiplayer_button.set_text(text)
        self.multiplayer_button.draw(self.screen)

    def _render_sound_toggle_button(self, game_state: GameState) -> None:
        text = c.SOUND_TOGGLE_BUTTON_TEXT_ON if not game_state.sound_manager.sound_muted else c.SOUND_TOGGLE_BUTTON_TEXT_OFF
        self.sound_button.set_text(text)
        self.sound_button.draw(self.screen)

    def _render_music_toggle_button(self, game_state: GameState) -> None:
        text = c.MUSIC_TOGGLE_BUTTON_TEXT_ON if not game_state.sound_manager.music_muted else c.MUSIC_TOGGLE_BUTTON_TEXT_OFF
        self.music_button.set_text(text)
        self.music_button.draw(self.screen)

    def _render_controls_info(self) -> None:
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
