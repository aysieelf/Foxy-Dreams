import pygame.sprite
from src.utils import constants as c


class Cloud(pygame.sprite.Sprite):
    """
    Class to represent a cloud in the game

    Attributes:
        image (pygame.Surface): The image of the cloud
        rect (pygame.Rect): The rectangle of the cloud
    """

    def __init__(self, player) -> None:
        """
        Initialize the cloud
        """
        pygame.sprite.Sprite.__init__(self)

        self.image: pygame.Surface = pygame.image.load("assets/images/cloud.png").convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(c.CLOUD_HITBOX_WIDTH, c.CLOUD_HITBOX_HEIGHT)
        self._set_position(player)

    def update(self) -> None:
        """
        Update the cloud
        """
        self.rect.x -= 1
        if self.rect.right < 0:
            self.rect.left = 800
            self.rect.y = 100

    def _set_position(self, player) -> None:
        """
        Set the position of the cloud
        """
        if player == "player1":
            self.image = pygame.transform.rotozoom(self.image, c.CLOUD_PLAYER1_ROTATION, 1)
            self.rect = self.image.get_rect()
            self.rect.x = c.CLOUD_PLAYER1_X
            self.rect.y = c.CLOUD_Y
        elif player == "player2":
            self.image = pygame.transform.rotozoom(self.image, c.CLOUD_PLAYER2_ROTATION, 1)
            self.rect = self.image.get_rect()
            self.rect.x = c.CLOUD_PLAYER2_X
            self.rect.y = c.CLOUD_Y
