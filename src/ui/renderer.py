from src.core.game_state import GameState

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

        game_state.all_sprites.draw(self.screen)
        game_state.bonus_star.particle_system.update()
        game_state.bonus_star.particle_system.draw(self.screen)

        pygame.display.flip()
