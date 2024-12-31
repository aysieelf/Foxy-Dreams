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
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.speed = c.BASE_SPEED * 0.35
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

        self._set_position(player)

    @property
    def hitbox(self):
        box = self.rect.copy()
        box.width = self.rect.width - c.CLOUD_HITBOX_WIDTH_DIFF
        box.height = self.rect.height - c.CLOUD_HITBOX_HEIGHT_DIFF
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
        if direction == "up" and self.hitbox.top > 0 - 4:
            self.rect.y -= self.speed
        elif direction == "down" and self.hitbox.bottom < c.HEIGHT + 4:
            self.rect.y += self.speed

    def handle_fox_collision(self, fox):
        if fox.hitbox.colliderect(self.hitbox):
            print(f"Collision detected!")
            print(f"Fox centery: {fox.hitbox.centery}")
            print(f"Cloud centery: {self.hitbox.centery}")
            print(f"Fox velocity before: {fox.velocity}")

            overlap_x = min(
                fox.hitbox.right - self.hitbox.left,
                self.hitbox.right - fox.hitbox.left,
            )
            overlap_y = min(
                fox.hitbox.bottom - self.hitbox.top,
                self.hitbox.bottom - fox.hitbox.top,
            )

            print(f"Overlap x: {overlap_x}, y: {overlap_y}")
            if overlap_x < overlap_y:
                if self.player == "player1":
                    if fox.hitbox.centerx > self.hitbox.centerx:
                        fox.velocity.x = abs(fox.velocity.x)
                elif self.player == "player2":
                    if fox.hitbox.centerx < self.hitbox.centerx:
                        fox.velocity.x = -abs(fox.velocity.x)

            else:
                if fox.hitbox.centery < self.hitbox.centery:
                    fox.rect.bottom = self.hitbox.top - c.FOX_HITBOX_DIFF * 0.75
                else:
                    fox.rect.top = self.hitbox.bottom + c.FOX_HITBOX_DIFF * 0.75
                fox.velocity.y *= -1

