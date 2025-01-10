import random

from src.core.fox import Fox
from src.utils import constants as c

import pygame.sprite


class Cloud(pygame.sprite.Sprite):
    """
    Class to represent a cloud in the game
    """

    def __init__(self, player: str, is_multiplayer: bool) -> None:
        super().__init__()
        self._player = player
        self._is_multiplayer = is_multiplayer
        self._speed = c.BASE_SPEED * 0.35
        self._collision_cooldown = 0
        self.image: pygame.Surface = pygame.image.load(
            "assets/images/cloud.png"
        ).convert_alpha()

        if player == "player1":
            self.image = pygame.transform.rotozoom(
                self.image, c.CLOUD_PLAYER1_ROTATION, 1
            )
        elif player == "player2":
            self.image = pygame.transform.rotozoom(
                self.image, c.CLOUD_PLAYER2_ROTATION, 1
            )

        self.rect = self.image.get_rect()

        self._shake_duration = 30
        self._shake_intensity = 1
        self._is_shaking = False
        self._shake_start = 0
        self._original_pos = None
        self._set_position(player)

    @property
    def player(self):
        return self._player

    @property
    def is_multiplayer(self):
        return self._is_multiplayer

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float) -> None:
        self._speed = value

    @property
    def collision_cooldown(self) -> int:
        return self._collision_cooldown

    @property
    def shake_duration(self) -> int:
        return self._shake_duration

    @property
    def shake_intensity(self) -> int:
        return self._shake_intensity

    @property
    def is_shaking(self) -> bool:
        return self._is_shaking

    @property
    def shake_start(self) -> int:
        return self._shake_start

    @property
    def original_pos(self) -> pygame.Rect:
        return self._original_pos

    @property
    def hitbox(self) -> pygame.Rect:
        """
        Get the hitbox of the cloud

        Returns:
            pygame.Rect: The hitbox of the cloud
        """
        box = self.rect.copy()
        box.width = self.rect.width - c.CLOUD_HITBOX_WIDTH_DIFF
        box.height = self.rect.height + c.CLOUD_HITBOX_HEIGHT_DIFF
        box.center = self.rect.center
        if self.player == "player1":
            box.left = self.rect.left
        elif self.player == "player2":
            box.right = self.rect.right
        return box

    def update(self, fox: Fox) -> None:
        """
        Update the cloud by moving it and shaking if necessary
        """
        self.update_shake()
        keys = pygame.key.get_pressed()

        # Player 1 (WASD)
        if self.player == "player1":
            if keys[pygame.K_w]:
                self.move("up")
            if keys[pygame.K_s]:
                self.move("down")

        # Player 2 (arrows)
        elif self.player == "player2" and self.is_multiplayer:
            if keys[pygame.K_UP]:
                self.move("up")
            if keys[pygame.K_DOWN]:
                self.move("down")

    def _set_position(self, player: str) -> None:
        """
        Set the position of the cloud
        """
        if player == "player1":
            self.rect.x = c.CLOUD_PLAYER1_X
            self.rect.y = c.CLOUD_Y
        elif player == "player2":
            self.rect.x = c.CLOUD_PLAYER2_X
            self.rect.y = c.CLOUD_Y

    def move(self, direction: str) -> None:
        """
        Move the cloud in the given direction

        Args:
            direction (str): The direction to move the cloud
        """
        current_speed = self.speed
        if self.collision_cooldown > 0:
            current_speed *= 0.5
            self._collision_cooldown -= 1

        if direction == "up" and self.hitbox.top > 0 - 4:
            self.rect.y -= self.speed
        elif direction == "down" and self.hitbox.bottom < c.HEIGHT + 4:
            self.rect.y += self.speed

    def handle_fox_collision(self, fox: Fox) -> bool:
        """
        Handle the collision between the cloud and the fox

        Args:
            fox (Fox): The fox to check collision with

        Returns:
            bool: Whether a collision occurred
        """
        if not fox.hitbox.colliderect(self.hitbox):
            return False

        self._init_collision_state()
        overlap_x, overlap_y = self._calculate_overlaps(fox)

        if overlap_x < overlap_y:
            self._handle_side_collision(fox)
        else:
            self._handle_vertical_collision(fox)

        return True

    def _init_collision_state(self) -> None:
        """
        Initialize the state of the cloud when a collision occurs
        """
        self._is_shaking = True
        self._shake_start = pygame.time.get_ticks()
        self._original_pos = self.rect.copy()

    def _calculate_overlaps(self, fox: Fox) -> tuple:
        """
        Calculate the overlaps between the cloud and the fox

        Args:
            fox (Fox): The fox to check overlaps with

        Returns:
            tuple: The overlaps in the x and y directions
        """
        overlap_x = min(
            fox.hitbox.right - self.hitbox.left,
            self.hitbox.right - fox.hitbox.left,
        )
        overlap_y = min(
            fox.hitbox.bottom - self.hitbox.top,
            self.hitbox.bottom - fox.hitbox.top,
        )
        return overlap_x, overlap_y

    def _handle_side_collision(self, fox: Fox) -> None:
        """
        Handle the side collision between the cloud and the fox
        """
        if self._is_valid_side_hit(fox):
            self._apply_side_bounce(fox)
        else:
            self._fix_invalid_side_hit(fox)

    def _is_valid_side_hit(self, fox: Fox) -> bool:
        """
        Check if the side hit is valid

        Args:
            fox (Fox): The fox to check the side hit with

        Returns:
            bool: Whether the side hit is valid
        """
        return (
            self.player == "player1" and fox.hitbox.centerx > self.hitbox.centerx
        ) or (self.player == "player2" and fox.hitbox.centerx < self.hitbox.centerx)

    def _apply_side_bounce(self, fox: Fox) -> None:
        """
        Apply the side bounce to the fox

        Args:
            fox (Fox): The fox to apply the side bounce to
        """
        vertical_bounce = self._calculate_vertical_bounce(fox)

        if self.player == "player1":
            fox.velocity.x = abs(fox.velocity.x)
        else:  # player2
            fox.velocity.x = -abs(fox.velocity.x)
        fox.velocity.y = vertical_bounce

        current_speed = fox.velocity.length()
        fox.velocity.scale_to_length(current_speed)

    def _calculate_vertical_bounce(self, fox: Fox) -> float:
        """
        Calculate the vertical bounce for the fox

        Args:
            fox (Fox): The fox to calculate the vertical bounce for

        Returns:
            float: The vertical bounce for the fox
        """
        relative_hit_point = (fox.hitbox.centery - self.hitbox.centery) / (
            self.hitbox.height / 2
        )
        min_vertical_component = 0.3
        vertical_bounce = relative_hit_point * c.BASE_SPEED

        if abs(vertical_bounce) < min_vertical_component * c.BASE_SPEED:
            vertical_bounce = (
                min_vertical_component
                * c.BASE_SPEED
                * (1 if vertical_bounce >= 0 else -1)
            )
        return vertical_bounce

    def _fix_invalid_side_hit(self, fox: Fox) -> None:
        """
        Fix an invalid side hit by moving the fox to the correct position

        Args:
            fox (Fox): The fox to fix the invalid side hit for
        """
        if self.player == "player1" and fox.hitbox.centerx > self.hitbox.centerx:
            fox.velocity.x = abs(fox.velocity.x)
        elif self.player == "player2" and fox.hitbox.centerx < self.hitbox.centerx:
            fox.velocity.x = -abs(fox.velocity.x)

    def _handle_vertical_collision(self, fox: Fox) -> None:
        """
        Handle the vertical collision between the cloud and the fox

        Args:
            fox (Fox): The fox to handle the vertical collision with
        """
        if fox.hitbox.centery < self.hitbox.centery:
            fox.rect.bottom = self.hitbox.top - c.FOX_HITBOX_DIFF * 0.75
        else:
            fox.rect.top = self.hitbox.bottom + c.FOX_HITBOX_DIFF * 0.75
        fox.velocity.y *= -1
        self._collision_cooldown = 3

    def update_shake(self) -> None:
        """
        Update the shake effect of the cloud
        """
        if not self.is_shaking:
            return

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.shake_start

        if elapsed > self.shake_duration:
            self._is_shaking = False
            self.rect.center = self.original_pos.center
            return

        offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
        offset_y = random.randint(-self.shake_intensity, self.shake_intensity)

        self.rect.centerx = self.original_pos.centerx + offset_x
        self.rect.centery = self.original_pos.centery + offset_y

    def reset(self) -> None:
        """
        Reset the cloud to its initial state
        """
        self._set_position(self.player)
        self._collision_cooldown = 0
        self.speed = c.BASE_SPEED * 0.35
        self._shake_duration = 20
        self._shake_intensity = 1
        self._is_shaking = False
        self._shake_start = 0
        self._original_pos = None
