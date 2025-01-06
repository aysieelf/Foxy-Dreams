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

    def render(self, game_state: GameState) -> None:
        """
        Render the game state on the screen

        Args:
            game_state (GameState): The current game state
        """
        self.screen.blit(self.background_image, (0, 0))

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
        pass

    def _render_playing_screen(self, game_state: GameState) -> None:
        game_state.all_sprites.draw(self.screen)
        game_state.bonus_star.particle_system.update()
        game_state.bonus_star.particle_system.draw(self.screen)

    def _render_pause_screen(self) -> None:
        pass

    def _render_game_over_leaderboard_screen(self, game_state: GameState) -> None:
        pass
