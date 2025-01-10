from random import randint, uniform


class Particle:
    """
    A simple particle class that represents a single particle in the particle system.
    """

    def __init__(self, x: int, y: int, color: tuple):
        self._x = x
        self._y = y
        self._velocity_x = uniform(-2, 2)
        self._velocity_y = uniform(-2, 2)
        self._lifetime = randint(30, 60)
        self._initial_lifetime = self._lifetime
        self._color = color
        self._size = 2

    def update(self) -> bool:
        """
        Update the particle's position and lifetime.

        Returns:
            bool: True if the particle is still alive, False otherwise.
        """
        self._x += self._velocity_x
        self._y += self._velocity_y

        self._lifetime -= 1

        alpha = int((self._lifetime / self._initial_lifetime) * 255)
        self._color = (*self._color[:3], alpha)

        return self._lifetime > 0
