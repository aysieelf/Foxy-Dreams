from random import choice

from src.core.ai_cloud import AICloud
from src.core.cloud import Cloud
from src.core.fox import Fox
from src.utils import constants as c

import pygame


class GameState:
    """
    Class to hold the game state
    """

    def __init__(self):
        self.base_speed = c.BASE_SPEED
        self.current_speed = self.base_speed
        self.max_speed = c.MAX_SPEED
        self.player1_score = 0
        self.player2_score = 0
        self.multiplayer = False

        self.fox = Fox(self.base_speed)
        self.cloud_player1 = Cloud("player1")
        self.cloud_player2 = Cloud("player2") if self.multiplayer else AICloud()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.fox, self.cloud_player1, self.cloud_player2)

    def update(self):
        winner = self.fox.update()
        self.cloud_player1.update(self.fox)
        self.cloud_player2.update(self.fox)
        self._check_for_winner(winner)
        self._check_for_fox_cloud_collision()

    def _check_for_winner(self, winner):
        if winner is not None:
            if winner == "player1":
                self.player1_score += 1

            elif winner == "player2":
                self.player2_score += 1

            self._fox_speed_update()
            self._play_again()

    def _fox_speed_update(self):
        player_score = max(self.player1_score, self.player2_score)
        if player_score > 0:
            new_speed = self.base_speed + (player_score / 30)
            self.current_speed = min(new_speed, self.max_speed)
        else:
            self.current_speed = self.base_speed

    def _play_again(self):
        self.fox.rect.center = (c.WIDTH // 2, c.HEIGHT // 2)
        direction_x = choice([-1, 1])
        direction_y = choice([1, -1])
        self.fox.velocity = pygame.math.Vector2(direction_x, direction_y)
        self.fox.velocity.scale_to_length(self.current_speed)
        self.fox.rect.x += self.fox.velocity.x
        self.fox.rect.y += self.fox.velocity.y

    def _check_for_fox_cloud_collision(self):
        if self.fox.hitbox.colliderect(self.cloud_player1.hitbox):
            self.fox.velocity.x *= -1

        if self.fox.hitbox.colliderect(self.cloud_player2.hitbox):
            self.fox.velocity.x *= -1
