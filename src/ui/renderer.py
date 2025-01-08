from src.core.game_state import GameState
from src.ui.button import Button
from src.utils import constants as c

import pygame

from src.utils.helpers import get_top_five_scores


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

        self.top_scores_image: pygame.Surface = pygame.image.load(
            "assets/images/top_scores.png"
        ).convert_alpha()

        self.start_button = Button(
            self.button_template.copy(),
            c.START_BUTTON_POS,
            c.START_BUTTON_TEXT,
            c.START_BUTTON_FONT,
            c.START_BUTTON_FONT_SIZE,
            c.START_BUTTON_TEXT_COLOR,
        )

        self.multiplayer_button = Button(
            self.button_template.copy(),
            c.MULTIPLAYER_TOGGLE_BUTTON_POS,
            c.MULTIPLAYER_TOGGLE_BUTTON_TEXT_OFF,
            c.MULTIPLAYER_TOGGLE_BUTTON_FONT,
            c.MULTIPLAYER_TOGGLE_BUTTON_FONT_SIZE,
            c.MULTIPLAYER_TOGGLE_BUTTON_TEXT_COLOR,
        )

        self.sound_button = Button(
            self.button_template.copy(),
            c.SOUND_TOGGLE_BUTTON_POS,
            c.SOUND_TOGGLE_BUTTON_TEXT_ON,
            c.SOUND_TOGGLE_BUTTON_FONT,
            c.SOUND_TOGGLE_BUTTON_FONT_SIZE,
            c.SOUND_TOGGLE_BUTTON_TEXT_COLOR,
        )

        self.music_button = Button(
            self.button_template.copy(),
            c.MUSIC_TOGGLE_BUTTON_POS,
            c.MUSIC_TOGGLE_BUTTON_TEXT_ON,
            c.MUSIC_TOGGLE_BUTTON_FONT,
            c.MUSIC_TOGGLE_BUTTON_FONT_SIZE,
            c.MUSIC_TOGGLE_BUTTON_TEXT_COLOR,
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
            self._render_pause_screen(game_state)
        elif game_state.current_state == c.GameStates.GAME_OVER_LEADERBOARD:
            self._render_game_over_leaderboard_screen(game_state)

        pygame.display.flip()

    def _render_start_screen(self, game_state: GameState) -> None:
        self.screen.blit(self.start_screen_image, (0, 0))
        self._render_start_button()
        self._render_multiplayer_toggle_button(game_state)
        self._render_sound_toggle_button(game_state, c.SOUND_TOGGLE_BUTTON_POS)
        self._render_music_toggle_button(game_state, c.MUSIC_TOGGLE_BUTTON_POS)
        self._render_controls_info()

    def _render_start_button(self) -> None:
        self.start_button.draw(self.screen)

    def _render_multiplayer_toggle_button(self, game_state: GameState) -> None:
        text = (
            c.MULTIPLAYER_TOGGLE_BUTTON_TEXT_ON
            if game_state.multiplayer
            else c.MULTIPLAYER_TOGGLE_BUTTON_TEXT_OFF
        )
        self.multiplayer_button.set_text(text)
        self.multiplayer_button.draw(self.screen)

    def _render_sound_toggle_button(self, game_state: GameState, new_pos=None) -> None:
        if new_pos:
            self.sound_button.set_position(new_pos)

        text = (
            c.SOUND_TOGGLE_BUTTON_TEXT_ON
            if not game_state.sound_manager.sound_muted
            else c.SOUND_TOGGLE_BUTTON_TEXT_OFF
        )
        self.sound_button.set_text(text)
        self.sound_button.draw(self.screen)

    def _render_music_toggle_button(self, game_state: GameState, new_pos=None) -> None:
        if new_pos:
            self.music_button.set_position(new_pos)

        text = (
            c.MUSIC_TOGGLE_BUTTON_TEXT_ON
            if not game_state.sound_manager.music_muted
            else c.MUSIC_TOGGLE_BUTTON_TEXT_OFF
        )
        self.music_button.set_text(text)
        self.music_button.draw(self.screen)

    def _render_controls_info(self) -> None:
        font = pygame.font.SysFont(c.CONTROLS_INFO_FONT, c.CONTROLS_INFO_FONT_SIZE)

        instruction_surface = font.render(
            c.CONTROLS_INFO_TEXT, True, c.CONTROLS_INFO_TEXT_COLOR
        )
        instruction_rect = instruction_surface.get_rect(center=c.CONTROLS_INFO_POS)
        self.screen.blit(instruction_surface, instruction_rect)

    def _render_playing_screen(self, game_state: GameState) -> None:
        self.screen.blit(self.background_image, (0, 0))
        self._render_score_board(game_state)
        self._render_current_level(game_state)
        game_state.all_sprites.draw(self.screen)
        game_state.bonus_star.particle_system.update()
        game_state.bonus_star.particle_system.draw(self.screen)

    def _render_score_board(self, game_state: GameState) -> None:
        font = pygame.font.SysFont(c.SCORE_FONT, c.SCORE_FONT_SIZE)
        text = font.render(
            f"PLAYER 1: {game_state.player1_score}",
            True,
            c.SCORE_TEXT_COLOR,
        )
        self.screen.blit(text, c.SCORE_POS_PLAYER1)

        text = font.render(
            f"Player 2: {game_state.player2_score}",
            True,
            c.SCORE_TEXT_COLOR,
        )
        self.screen.blit(text, c.SCORE_POS_PLAYER2)

    def _render_current_level(self, game_state: GameState) -> None:
        font = pygame.font.SysFont(c.LEVEL_FONT, c.LEVEL_FONT_SIZE)
        text = font.render(
            f"{c.LEVEL_TEXT} {game_state.level}",
            True,
            c.SCORE_TEXT_COLOR,
        )
        self.screen.blit(text, c.LEVEL_POS)

    def _render_pause_screen(self, game_state) -> None:
        self.screen.blit(self.background_image, (0, 0))
        self._render_sound_toggle_button(game_state, c.PAUSE_SOUND_TOGGLE_BUTTON_POS)
        self._render_music_toggle_button(game_state, c.PAUSE_MUSIC_TOGGLE_BUTTON_POS)
        self._render_pause_title()
        self._render_pause_info()

    def _render_pause_title(self):
        font = pygame.font.SysFont(c.PAUSE_FONT, c.PAUSE_FONT_SIZE)
        text = font.render(c.PAUSE_TEXT, True, c.PAUSE_TEXT_COLOR)
        text_rect = text.get_rect(center=c.PAUSE_TEXT_POS)
        self.screen.blit(text, text_rect)

    def _render_pause_info(self):
        font = pygame.font.SysFont(c.PAUSE_SUBTEXT_FONT, c.PAUSE_SUBTEXT_FONT_SIZE)
        text = font.render(c.PAUSE_SUBTEXT, True, c.PAUSE_SUBTEXT_COLOR)
        text_rect = text.get_rect(center=c.PAUSE_SUBTEXT_POS)
        self.screen.blit(text, text_rect)

    def _render_game_over_leaderboard_screen(self, game_state: GameState) -> None:
        self.screen.blit(self.background_image, (0, 0))
        self._render_text()
        self._current_score(game_state)
        self._top_scores(game_state)

    def _render_text(self):
        font = pygame.font.SysFont(c.GAME_OVER_FONT, c.GAME_OVER_FONT_SIZE)
        text = font.render(c.GAME_OVER_TITLE, True, c.GAME_OVER_TEXT_COLOR)
        text_rect = text.get_rect(center=c.GAME_OVER_POS)
        self.screen.blit(text, text_rect)

        font = pygame.font.SysFont(c.GAME_OVER_SUBTEXT_FONT, c.GAME_OVER_SUBTEXT_FONT_SIZE)
        text = font.render(c.GAME_OVER_SUBTEXT, True, c.GAME_OVER_SUBTEXT_COLOR)
        text_rect = text.get_rect(center=c.GAME_OVER_SUBTEXT_POS)
        self.screen.blit(text, text_rect)

    def _current_score(self, game_state: GameState):
        font = pygame.font.SysFont(c.GAME_OVER_CURRENT_SCORE_FONT, c.GAME_OVER_CURRENT_SCORE_FONT_SIZE)
        text = font.render(
            f"Player 1: {game_state.player1_score}",
            True,
            c.GAME_OVER_CURRENT_SCORE_TEXT_COLOR,
        )
        self.screen.blit(text, c.GAME_OVER_CURRENT_SCORE_P1_POS)

        if game_state.multiplayer:
            text = font.render(
                f"Player 2: {game_state.player2_score}",
                True,
                c.GAME_OVER_CURRENT_SCORE_TEXT_COLOR,
            )
            self.screen.blit(text, c.GAME_OVER_CURRENT_SCORE_P2_POS)

    def _top_scores(self, game_state: GameState):
        image_rect = self.top_scores_image.get_rect(center=c.TOP_SCORES_RECT_POS)
        self.screen.blit(self.top_scores_image, image_rect)

        font = pygame.font.SysFont(c.TOP_SCORES_FONT, c.TOP_SCORES_FONT_SIZE, bold=True)
        text = font.render(
            c.TOP_SCORES_TEXT,
            True,
            c.TOP_SCORES_TEXT_COLOR,
        )
        text_rect = text.get_rect(center=c.TOP_SCORES_POS)
        self.screen.blit(text, text_rect)

        top_scores = get_top_five_scores()
        top_scores_str = [f"{score.date}: {score.score} points" for score in top_scores]

        for i, score in enumerate(top_scores_str):
            text = font.render(
                score,
                True,
                c.TOP_SCORES_TEXT_COLOR,
            )
            text_rect = text.get_rect(center=(c.WIDTH // 2, c.HEIGHT // 2 + i * 30))
            self.screen.blit(text, text_rect)
