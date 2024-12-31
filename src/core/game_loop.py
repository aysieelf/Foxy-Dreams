from src.core.game_state import GameState
from src.event_handler import EventHandler
from src.ui.renderer import Renderer

import pygame


def game_loop(
    screen: pygame.Surface, game_state: GameState, clock: pygame.time.Clock
) -> None:
    """
    Handles the game loop

    Args:
        screen (pygame.Surface): The screen to render
        game_state (GameState): The current game state
        clock (pygame.time.Clock): The game clock
    """
    event_handler = EventHandler(game_state)
    renderer = Renderer(screen)

    while True:
        clock.tick(0)
        game_state.update()
        game_state.cloud_player1.update(game_state.fox)
        game_state.cloud_player2.update(game_state.fox)
        if not event_handler.handle_events():
            break

        renderer.render(game_state)
