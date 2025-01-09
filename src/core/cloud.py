import random

from src.utils import constants as c

import pygame.sprite


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
        super().__init__()
        self.player = player
        self.speed = c.BASE_SPEED * 0.35
        self.collision_cooldown = 0
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

        self.shake_duration = 20
        self.shake_intensity = 1
        self.is_shaking = False
        self.shake_start = 0
        self.original_pos = None
        self._set_position(player)

    @property
    def hitbox(self):
        box = self.rect.copy()
        box.width = self.rect.width - c.CLOUD_HITBOX_WIDTH_DIFF
        box.height = self.rect.height + c.CLOUD_HITBOX_HEIGHT_DIFF
        box.center = self.rect.center
        if self.player == "player1":
            box.left = self.rect.left
        elif self.player == "player2":
            box.right = self.rect.right
        return box

    def update(self, fox) -> None:
        """
        Update the cloud
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
        elif self.player == "player2":
            if keys[pygame.K_UP]:
                self.move("up")
            if keys[pygame.K_DOWN]:
                self.move("down")

    def _set_position(self, player) -> None:
        """
        Set the position of the cloud
        """
        if player == "player1":
            self.rect.x = c.CLOUD_PLAYER1_X
            self.rect.y = c.CLOUD_Y
        elif player == "player2":
            self.rect.x = c.CLOUD_PLAYER2_X
            self.rect.y = c.CLOUD_Y

    def move(self, direction):
        current_speed = self.speed
        if self.collision_cooldown > 0:
            current_speed *= 0.5
            self.collision_cooldown -= 1

        if direction == "up" and self.hitbox.top > 0 - 4:
            self.rect.y -= self.speed
        elif direction == "down" and self.hitbox.bottom < c.HEIGHT + 4:
            self.rect.y += self.speed

    def handle_fox_collision(self, fox):
        if not fox.hitbox.colliderect(self.hitbox):
            return False

        self._init_collision_state()
        overlap_x, overlap_y = self._calculate_overlaps(fox)

        if overlap_x < overlap_y:
            self._handle_side_collision(fox)
        else:
            self._handle_vertical_collision(fox)

        return True

    def _init_collision_state(self):
        self.is_shaking = True
        self.shake_start = pygame.time.get_ticks()
        self.original_pos = self.rect.copy()

    def _calculate_overlaps(self, fox):
        overlap_x = min(
            fox.hitbox.right - self.hitbox.left,
            self.hitbox.right - fox.hitbox.left,
        )
        overlap_y = min(
            fox.hitbox.bottom - self.hitbox.top,
            self.hitbox.bottom - fox.hitbox.top,
        )
        return overlap_x, overlap_y

    def _handle_side_collision(self, fox):
        if self._is_valid_side_hit(fox):
            self._apply_side_bounce(fox)
        else:
            self._fix_invalid_side_hit(fox)

    def _is_valid_side_hit(self, fox):
        return (
                self.player == "player1" and fox.hitbox.centerx > self.hitbox.centerx
        ) or (
                self.player == "player2" and fox.hitbox.centerx < self.hitbox.centerx
        )

    def _apply_side_bounce(self, fox):
        vertical_bounce = self._calculate_vertical_bounce(fox)

        if self.player == "player1":
            fox.velocity.x = abs(fox.velocity.x)
        else:  # player2
            fox.velocity.x = -abs(fox.velocity.x)
        fox.velocity.y = vertical_bounce

        current_speed = fox.velocity.length()
        fox.velocity.scale_to_length(current_speed)

    def _calculate_vertical_bounce(self, fox):
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

    def _fix_invalid_side_hit(self, fox):
        if (
                self.player == "player1"
                and fox.hitbox.centerx > self.hitbox.centerx
        ):
            fox.velocity.x = abs(fox.velocity.x)
        elif (
                self.player == "player2"
                and fox.hitbox.centerx < self.hitbox.centerx
        ):
            fox.velocity.x = -abs(fox.velocity.x)

    def _handle_vertical_collision(self, fox):
        if fox.hitbox.centery < self.hitbox.centery:
            fox.rect.bottom = self.hitbox.top - c.FOX_HITBOX_DIFF * 0.75
        else:
            fox.rect.top = self.hitbox.bottom + c.FOX_HITBOX_DIFF * 0.75
        fox.velocity.y *= -1
        self.collision_cooldown = 3

    def reset(self):
        self._set_position(self.player)
        self.collision_cooldown = 0
        self.speed = c.BASE_SPEED * 0.35

    def update_shake(self):
        if not self.is_shaking:
            return

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.shake_start

        if elapsed > self.shake_duration:
            self.is_shaking = False
            self.rect.center = self.original_pos.center
            return

        offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
        offset_y = random.randint(-self.shake_intensity, self.shake_intensity)

        self.rect.centerx = self.original_pos.centerx + offset_x
        self.rect.centery = self.original_pos.centery + offset_y
