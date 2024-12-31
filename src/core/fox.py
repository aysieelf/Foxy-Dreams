from src.utils import constants as c

import pygame.sprite


class Fox(pygame.sprite.Sprite):
    def __init__(self, initial_speed):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load("assets/images/fox.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (c.WIDTH // 2, c.HEIGHT // 2)
        self.radius = (self.rect.width - c.FOX_HITBOX_DIFF) // 2

        self.velocity = pygame.math.Vector2(1, 0.5)
        self.velocity.scale_to_length(initial_speed)
        self.angle = 0

    @property
    def hitbox(self):
        diameter = self.rect.width - c.FOX_HITBOX_DIFF
        box = pygame.Rect(0, 0, diameter, diameter)
        box.center = self.rect.center
        return box

    def update(self) -> str | None:
        self._rotate_image()
        self._move_fox()
        max_allowed_speed = self.velocity.length() + 4
        self.velocity = self.velocity.clamp_magnitude(c.BASE_SPEED, max_allowed_speed)
        return self._check_for_collision()

    def _move_fox(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def _rotate_image(self):
        self.angle += 0.1
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def _check_for_collision(self):
        # Check if fox is out
        if self.rect.right < 0:
            return "player1"
        if self.rect.left > c.WIDTH:
            return "player2"

        # Check if fox should change direction
        if self.hitbox.top <= -2 or self.hitbox.bottom >= c.HEIGHT:
            if self.rect.top <= 0:
                self.rect.top = 0
            else:
                self.rect.bottom = c.HEIGHT
            self.velocity.y *= -1
            return
