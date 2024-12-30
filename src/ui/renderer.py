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

        # TODO - debugging square
        pygame.draw.rect(self.screen, (255, 0, 0), game_state.cloud_player1.hitbox, 1)
        pygame.draw.rect(self.screen, (0, 255, 0), game_state.cloud_player2.hitbox, 1)


        pygame.display.flip()
