from src.core.fox import Fox
from src.effects.particle_system import ParticleSystem
from src.utils import constants as c
from src.utils.helpers import get_random_position

import pygame.sprite


class BonusStar(pygame.sprite.Sprite):
    """
    Class to represent a bonus star in the game
    """
    def __init__(self, sprite_group: pygame.sprite.Group, game_state: "GameState") -> None:
        super().__init__()
        self.game_state = game_state
        self._active = False
        self.sprite_group = sprite_group
        self._collision_cooldown = 0
        self.particle_system = ParticleSystem()

        self.image = pygame.image.load("assets/images/star-bonus.png").convert_alpha()
        self.rect = self.image.get_rect()

    @property
    def active(self) -> bool:
        return self._active

    @property
    def collision_cooldown(self) -> int:
        return self._collision_cooldown

    @property
    def hitbox(self) -> pygame.Rect:
        """
        Get the hitbox of the bonus star

        Returns:
            pygame.Rect: The hitbox of the bonus star
        """
        box = self.rect.copy()
        box.width = self.rect.width - c.BONUS_HITBOX_DIFF
        box.height = self.rect.height - c.BONUS_HITBOX_DIFF
        box.center = self.rect.center
        return box

    def spawn(self) -> None:
        """
        Spawn the bonus star. Set the position and add it to the sprite group.
        """
        if self.game_state.current_state != c.GameStates.PLAYING:
            return

        self._active = True
        self._set_pos()
        self.sprite_group.add(self)
        pygame.time.set_timer(c.BONUS_DE_SPAWN_EVENT, c.BONUS_LIFETIME)

    def despawn(self) -> None:
        """
        Despawn the bonus star. Remove it from the sprite group.
        """
        if self.game_state.current_state != c.GameStates.PLAYING:
            return

        self._active = False
        self.sprite_group.remove(self)
        self._collision_cooldown = 0
        pygame.time.set_timer(c.BONUS_DE_SPAWN_EVENT, 0)

    def _set_pos(self) -> pygame.Rect:
        """
        Set the position of the bonus star to a random position on the screen.

        Returns:
            pygame.Rect: The rectangle of the bonus star
        """
        self.rect.center = get_random_position()
        return self.rect

    def handle_fox_collision(self, fox: Fox) -> int:
        """
        Handle the collision between the fox and the bonus star.

        Args:
            fox (Fox): The fox object to check collision with

        Returns:
            int: The number of bonus points to add to the score
        """
        if not self._active or self.collision_cooldown > 0:
            return 0

        if fox.hitbox.colliderect(self.hitbox):
            self.particle_system.spawn_particles(
                *self.rect.center, c.STAR_PARTICLES_COLOR
            )
            self._collision_cooldown = 5
            self.despawn()
            return c.BONUS_POINTS

        return 0
