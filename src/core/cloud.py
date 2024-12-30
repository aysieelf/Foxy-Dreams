import pygame.sprite


class Cloud(pygame.sprite.Sprite):
    """
    Class to represent a cloud in the game

    Attributes:
        image (pygame.Surface): The image of the cloud
        rect (pygame.Rect): The rectangle of the cloud
    """

    def __init__(self) -> None:
        """
        Initialize the cloud
        """
        pygame.sprite.Sprite.__init__(self)

        self.image: pygame.Surface = pygame.image.load("assets/images/cloud.png").convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect()

    def update(self) -> None:
        """
        Update the cloud
        """
        self.rect.x -= 1
        if self.rect.right < 0:
            self.rect.left = 800
            self.rect.y = 100