import pygame.sprite
from src.utils import constants as c
from src.utils.helpers import get_random_position


class BonusStar(pygame.sprite.Sprite):
    def __init__(self, sprite_group):
        pygame.sprite.Sprite.__init__(self)
        self._active = False
        self.sprite_group = sprite_group

        self.image = pygame.image.load("assets/images/star-bonus.png").convert_alpha()
        self.rect = self.image.get_rect()


    def spawn(self):
        self._active = True
        self._set_pos()
        self.sprite_group.add(self)
        print("Spawned")
        pygame.time.set_timer(c.BONUS_DE_SPAWN_EVENT, c.BONUS_LIFETIME)

    def despawn(self):
        self._active = False
        print("Despawned")
        self.sprite_group.remove(self)
        pygame.time.set_timer(c.BONUS_DE_SPAWN_EVENT, 0)

    def _set_pos(self):
        self.rect = get_random_position()
        return self.rect
