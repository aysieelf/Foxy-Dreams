from src.core.cloud import Cloud
from src.utils import constants as c


class AICloud(Cloud):
    def __init__(self):
        super().__init__("player2")
        self.speed = c.BASE_SPEED * 0.8
        self.dead_zone = 10
        self.reaction_delay = 2
        self.delay_counter = 0

    def update(self, fox):
        self._handle_ai_movement(fox)

    def _handle_ai_movement(self, fox):
        self.delay_counter += 1

        if self.delay_counter >= self.reaction_delay:
            self.delay_counter = 0
            distance = fox.rect.centery - self.rect.centery

            if abs(distance) > self.dead_zone:
                direction = "down" if distance > 0 else "up"

                speed_factor = min(abs(distance) / 100, 1.0)
                self._move_with_speed(direction, speed_factor)

    def _move_with_speed(self, direction, speed_factor):
        if direction == "up" and self.hitbox.top > 0 - 4:
            self.rect.y -= self.speed * speed_factor
        elif direction == "down" and self.hitbox.bottom < c.HEIGHT + 4:
            self.rect.y += self.speed * speed_factor