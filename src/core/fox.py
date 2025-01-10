from src.core.sound_manager import SoundManager
from src.utils import constants as c

import pygame.sprite


class Fox(pygame.sprite.Sprite):
    """Fox class that represents the fox in the game."""
    def __init__(self, initial_speed: float) -> None:
        super().__init__()
        self._load_image()
        self.velocity = pygame.math.Vector2(1, 0.5)
        self.velocity.scale_to_length(initial_speed)
        self.angle = 0

    @property
    def hitbox(self) -> pygame.Rect:
        """
        Return the hitbox of the fox.

        Returns:
            pygame.Rect: The hitbox of the fox.
        """
        diameter = self.rect.width - c.FOX_HITBOX_DIFF
        box = pygame.Rect(0, 0, diameter, diameter)
        box.center = self.rect.center
        return box

    def _load_image(self) -> None:
        """Load the image of the fox."""
        self.original_image = pygame.image.load("assets/images/fox.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (c.WIDTH // 2, c.HEIGHT // 2)
        self.radius = (self.rect.width - c.FOX_HITBOX_DIFF) // 2

    def update(self, sound_manager: SoundManager) -> str | None:
        """
        Update the fox: rotate the image, move the fox and check for collision.

        Args:
            sound_manager (SoundManager): The sound manager object.

        Returns:
            str | None: The winner of the game, if there is one.
        """
        self._rotate_image()
        self._move_fox()
        max_allowed_speed = self.velocity.length() + 4
        self.velocity = self.velocity.clamp_magnitude(c.BASE_SPEED, max_allowed_speed)
        return self._check_for_collision(sound_manager)

    def _move_fox(self) -> None:
        """ Move the fox. """
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def _rotate_image(self) -> None:
        """ Rotate the image of the fox. """
        self.angle += 0.1
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def _check_for_collision(self, sound_manager: SoundManager) -> str | None:
        """
        Check if the fox has collided with the screen borders.
        If so, change direction and play sound.

        Args:
            sound_manager (SoundManager): The sound manager object.

        Returns:
            str | None: The winner of the game, if there is one.
        """
        margin = 50
        if self.rect.right < margin:
            sound_manager.play_sound("fox-fly-away")
            if self.rect.right < 0:
                return "player2"

        if self.rect.left > c.WIDTH - margin:
            sound_manager.play_sound("fox-fly-away")
            if self.rect.left > c.WIDTH:
                return "player1"

        # Check if fox should change direction
        if self.hitbox.top <= -2 or self.hitbox.bottom >= c.HEIGHT:
            if self.rect.top <= 0:
                self.rect.top = 0
            else:
                self.rect.bottom = c.HEIGHT
            self.velocity.y *= -1
            return
