import pygame.sprite

from src.effects.particle_system import ParticleSystem
from src.utils import constants as c
from src.utils.helpers import get_random_position


class BonusStar(pygame.sprite.Sprite):
    def __init__(self, sprite_group):
        pygame.sprite.Sprite.__init__(self)
        self._active = False
        self.sprite_group = sprite_group
        self.collision_cooldown = 0
        self.particle_system = ParticleSystem()

        self.image = pygame.image.load("assets/images/star-bonus.png").convert_alpha()
        self.rect = self.image.get_rect()

    @property
    def hitbox(self):
        box = self.rect.copy()
        box.width = self.rect.width - c.BONUS_HITBOX_DIFF
        box.height = self.rect.height - c.BONUS_HITBOX_DIFF
        box.center = self.rect.center
        return box

    def spawn(self):
        self._active = True
        self._set_pos()
        self.sprite_group.add(self)
        pygame.time.set_timer(c.BONUS_DE_SPAWN_EVENT, c.BONUS_LIFETIME)

    def despawn(self):
        self._active = False
        self.sprite_group.remove(self)
        self.collision_cooldown = 0
        pygame.time.set_timer(c.BONUS_DE_SPAWN_EVENT, 0)

    def _set_pos(self):
        self.rect.center = get_random_position()
        return self.rect

    def handle_fox_collision(self, fox):
        # TODO: Add particles
        if not self._active:
            return 0

        if self.collision_cooldown > 0:
            return 0

        if fox.hitbox.colliderect(self.hitbox):
            self.particle_system.spawn_particles(*self.rect.center, c.STAR_PARTICLES)
            self.collision_cooldown = 5
            self.despawn()
            return c.BONUS_POINTS

        return 0
