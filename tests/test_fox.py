import unittest
from unittest.mock import patch, Mock, PropertyMock, MagicMock

import pygame

from src.core.fox import Fox
from src.utils import constants as c


class FoxShould(unittest.TestCase):
    def setUp(self):
        patcher = patch.object(Fox, '_load_image')
        patcher.start()
        self.addCleanup(patcher.stop)

        self.fox = Fox(c.BASE_SPEED)
        self.fox.rect = Mock()
        self.fox.rect.width = 64
        self.fox.rect.height = 64
        self.fox.rect.center = (c.WIDTH // 2, c.HEIGHT // 2)
        self.fox.radius = (64 - c.FOX_HITBOX_DIFF) // 2

    def test_init_initializesSuccessfully(self):
        self.assertIsNotNone(self.fox)

    def test_init_callsLoadImage(self):
        self.fox._load_image.assert_called_once()

    def test_init_setsVelocity(self):
        self.assertIsNotNone(self.fox.velocity)

    def test_init_setsVelocityLength(self):
        self.assertEqual(c.BASE_SPEED, self.fox.velocity.length())

    def test_init_setsAngle(self):
        self.assertEqual(0, self.fox.angle)

    def test_hitbox_returnsCorrectHitbox(self):
        hitbox = self.fox.hitbox
        self.assertEqual(64 - c.FOX_HITBOX_DIFF, hitbox.width)
        self.assertEqual(64 - c.FOX_HITBOX_DIFF, hitbox.height)
        self.assertEqual(self.fox.rect.center, hitbox.center)

    def test_update_callsRotateImage(self):
        with (patch.object(self.fox, '_rotate_image') as mock_rotate_image,
              patch.object(self.fox, '_move_fox'),
              patch.object(self.fox, '_check_for_collision'),
              ):
            self.fox.update(None)
            mock_rotate_image.assert_called_once()

    def test_update_callsMoveFox(self):
        with (patch.object(self.fox, '_rotate_image'),
              patch.object(self.fox, '_move_fox') as mock_move_fox,
              patch.object(self.fox, '_check_for_collision'),
              ):
            self.fox.update(None)
            mock_move_fox.assert_called_once()

    def test_update_callsCheckForCollision(self):
        with (patch.object(self.fox, '_rotate_image'),
              patch.object(self.fox, '_move_fox'),
              patch.object(self.fox, '_check_for_collision') as mock_check_for_collision,
              ):
            self.fox.update(None)
            mock_check_for_collision.assert_called_once()

    def test_moveFox_movesFox(self):
        self.fox.velocity = pygame.math.Vector2(1, 1)
        self.fox.rect.x = 0
        self.fox.rect.y = 0

        self.fox._move_fox()

        self.assertEqual(1, self.fox.rect.x)
        self.assertEqual(1, self.fox.rect.y)

    def test_rotateImage_rotatesImage(self):
        self.fox.original_image = pygame.Surface((64, 64))
        self.fox.image = self.fox.original_image
        self.fox.rect = self.fox.image.get_rect()
        self.fox.rect.center = (c.WIDTH // 2, c.HEIGHT // 2)
        self.fox.angle = 0

        self.fox._rotate_image()

        self.assertNotEqual(self.fox.image, self.fox.original_image)
        self.assertNotEqual(self.fox.rect, self.fox.image.get_rect())

    def test_checkForCollision_returnsPlayer1_whenFoxIsOutOfBounds(self):
        self.fox.rect.left = c.WIDTH + 10
        self.fox.rect.right = 0

        sound_manager = Mock()
        sound_manager.play_sound = Mock()

        result = self.fox._check_for_collision(sound_manager)

        self.assertEqual("player1", result)

    def test_checkForCollision_returnsPlayer2_whenFoxIsOutOfBounds(self):
        self.fox.rect.left = 0
        self.fox.rect.right = -10

        sound_manager = Mock()
        sound_manager.play_sound = Mock()

        result = self.fox._check_for_collision(sound_manager)

        self.assertEqual("player2", result)

    def test_checkForCollision_playsSound_whenFoxIsOutOfBounds(self):
        self.fox.rect.left = 0
        self.fox.rect.right = -10

        sound_manager = Mock()
        sound_manager.play_sound = Mock()

        self.fox._check_for_collision(sound_manager)

        sound_manager.play_sound.assert_called_once()

    def test_checkForCollision_returnsNone_whenFoxIsNotOutOfBounds(self):
        self.fox.rect.left = 0
        self.fox.rect.right = c.WIDTH

        sound_manager = Mock()
        sound_manager.play_sound = Mock()

        result = self.fox._check_for_collision(sound_manager)

        self.assertIsNone(result)
