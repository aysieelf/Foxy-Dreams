from src.utils import constants as c

import pygame


def create_rectangle(
    screen: pygame.Surface,
    color: tuple,
    x: int,
    y: int,
    width: int,
    height: int,
) -> None:
    """
    Create a rectangle on the screen.

    Args:
        screen (pygame.Surface): The screen to draw on
        color (tuple): The color of the rectangle
        x (int): The x position of the rectangle
        y (int): The y position of the rectangle
        width (int): The width of the rectangle
        height (int): The height of the rectangle
    """
    pygame.draw.rect(screen, color, (x, y, width, height))