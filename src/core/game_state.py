import pygame

from src.core.fox import Fox


class GameState:
    """
    Class to hold the game state
    """

    def __init__(self):
        self.fox = Fox()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.fox)
