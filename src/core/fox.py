import pygame.sprite
from src.utils import constants as c


class Fox(pygame.sprite.Sprite):
    def __init__(self, initial_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/fox.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (c.WIDTH//2, c.HEIGHT//2)

        self.velocity = pygame.math.Vector2(1, 1)
        self.velocity.scale_to_length(initial_speed)


    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        return self._check_for_collision()

    def _check_for_collision(self):
        # Check if fox is out
        if self.rect.right < 0:
            return "player1"
        if self.rect.left > c.WIDTH:
            return "player2"

        # Check if fox should change direction
        if self.rect.top <= 0 or self.rect.bottom >= c.HEIGHT:
            self.velocity.y *= -1
            return
