import pygame.sprite
from src.utils import constants as c
from src.utils.helpers import get_random_position


class BonusStar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._spawn_duration_timer = 0
        self._between_spawns_timer = 0
        self._active = False

        self.image = pygame.image.load("assets/images/star-bonus.png").convert_alpha()
        self.rect = self.image.get_rect()


    def update(self):
        if not self._active:
            if self._between_spawns_timer <= 1:
                self._active = True
                self._set_pos()
                self._spawn_duration_timer = c.BONUS_SPAWN_DURATION
            self._between_spawns_timer = 0

        else:
            if self._spawn_duration_timer <= 1:
                self._active = False

                self._between_spawns_timer = c.BONUS_BETWEEN_SPAWNS_TIMER
            self._spawn_duration_timer -= 1

    def _set_pos(self):
        self.rect = get_random_position()
        return self.rect


