from src.core.cloud import Cloud
from src.core.fox import Fox
from src.utils import constants as c


class AICloud(Cloud):
    """
    A class to represent an AI cloud.
    """
    def __init__(self) -> None:
        super().__init__("player2", is_multiplayer=False)
        self._speed = c.BASE_SPEED * 0.8
        self._dead_zone = 10
        self._reaction_delay = 2
        self._delay_counter = 0

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float) -> None:
        self._speed = value

    @property
    def dead_zone(self) -> int:
        return self._dead_zone

    @property
    def reaction_delay(self) -> int:
        return self._reaction_delay

    @property
    def delay_counter(self) -> int:
        return self._delay_counter

    def update(self, fox: Fox) -> None:
        """
        Update the AI cloud's position based on the fox's position.

        Args:
            fox (Fox): The fox object to track.
        """
        super().update(fox)
        self._handle_ai_movement(fox)

    def _handle_ai_movement(self, fox: Fox) -> None:
        """
        Handle the AI cloud's movement based on the fox's position.

        Args:
            fox (Fox): The fox object to track.
        """
        self._delay_counter += 1

        if self.delay_counter >= self.reaction_delay:
            self._delay_counter = 0
            distance = fox.rect.centery - self.rect.centery

            if abs(distance) > self.dead_zone:
                direction = "down" if distance > 0 else "up"

                speed_factor = min(abs(distance) / 100, 1.0)
                self._move_with_speed(direction, speed_factor)

    def _move_with_speed(self, direction: str, speed_factor: float) -> None:
        """
        Move the AI cloud in the specified direction with the given speed factor.

        Args:
            direction (str): The direction to move the AI cloud.
            speed_factor (float): The speed factor to apply to the AI cloud's movement.
        """
        adjusted_speed_factor = min(speed_factor * 0.8, 0.8)

        if direction == "up" and self.hitbox.top > 0 - 4:
            self.rect.y -= self.speed * adjusted_speed_factor
        elif direction == "down" and self.hitbox.bottom < c.HEIGHT + 4:
            self.rect.y += self.speed * adjusted_speed_factor
