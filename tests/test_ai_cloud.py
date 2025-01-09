import unittest
from unittest.mock import Mock, patch, PropertyMock

import pygame

from src.core.ai_cloud import AICloud
from src.utils import constants as c


class AICloudShould(unittest.TestCase):
    @patch('pygame.transform.rotozoom')
    @patch('pygame.image.load')
    def setUp(self, mock_load, mock_rotozoom):
        mock_surface = Mock()
        mock_converted_surface = Mock()
        mock_rotated_surface = Mock()

        mock_surface.convert_alpha.return_value = mock_converted_surface
        mock_load.return_value = mock_surface
        mock_rotozoom.return_value = mock_rotated_surface

        mock_rotated_surface.get_rect.return_value = Mock()

        self.ai_cloud = AICloud()

    def test_init_initializesSuccessfully(self):
        self.assertIsNotNone(self.ai_cloud)

    def test_init_setsSpeed(self):
        self.assertEqual(c.BASE_SPEED * 0.8, self.ai_cloud.speed)

    def test_init_setsDeadZone(self):
        self.assertEqual(10, self.ai_cloud.dead_zone)

    def test_init_setsReactionDelay(self):
        self.assertEqual(2, self.ai_cloud.reaction_delay)

    def test_init_setsDelayCounter(self):
        self.assertEqual(0, self.ai_cloud.delay_counter)

    @patch('src.core.cloud.Cloud.update')
    def test_update_callsHandleAIMovement(self, mock_super_update):
        with patch.object(self.ai_cloud, "_handle_ai_movement") as mock_handle_ai_movement:
            fox = Mock()
            self.ai_cloud.update(fox)

            mock_super_update.assert_called_once_with(fox)
            mock_handle_ai_movement.assert_called_once_with(fox)

    def test_handleAiMovement_incrementsDelayCounter(self):
        self.ai_cloud.delay_counter = 0

        self.ai_cloud._handle_ai_movement(None)
        self.assertEqual(1, self.ai_cloud.delay_counter)

    def test_handleAiMovement_setsDelayCounterToZero_whenCounterIsEqualToReaction(self):
        with patch.object(self.ai_cloud, "_move_with_speed"):
            fox = Mock()
            fox.rect.centery = 9
            self.ai_cloud.rect.centery = 0
            self.ai_cloud.delay_counter = 2

            self.ai_cloud._handle_ai_movement(fox)
            self.assertEqual(0, self.ai_cloud.delay_counter)

    def test_handleAiMovement_movesUp_whenFoxIsAboveCloud(self):
        with patch.object(self.ai_cloud, "_move_with_speed") as mock_move_with_speed:
            fox = Mock()
            fox.rect.centery = -100
            self.ai_cloud.rect.centery = 10
            self.ai_cloud.delay_counter = 2

            self.ai_cloud._handle_ai_movement(fox)
            mock_move_with_speed.assert_called_once_with("up", 1.0)

    def test_handleAiMovement_movesDown_whenFoxIsBelowCloud(self):
        with patch.object(self.ai_cloud, "_move_with_speed") as mock_move_with_speed:
            fox = Mock()
            fox.rect.centery = 110
            self.ai_cloud.rect.centery = 10
            self.ai_cloud.delay_counter = 2

            self.ai_cloud._handle_ai_movement(fox)
            mock_move_with_speed.assert_called_once_with("down", 1.0)

    def test_handleAiMovement_doesNotMove_whenFoxIsWithinDeadZone(self):
        with patch.object(self.ai_cloud, "_move_with_speed") as mock_move_with_speed:
            fox = Mock()
            fox.rect.centery = 10
            self.ai_cloud.rect.centery = 10
            self.ai_cloud.delay_counter = 2

            self.ai_cloud._handle_ai_movement(fox)
            mock_move_with_speed.assert_not_called()

    def test_moveWithSpeed_movesUp_whenHitBoxTopIsGreaterThanNegativeFour(self):
        mock_hitbox = Mock()
        mock_hitbox.top = 0

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox_property:
            mock_hitbox_property.return_value = mock_hitbox

            initial_y = self.ai_cloud.rect.y
            speed_factor = 1.0

            self.ai_cloud._move_with_speed("up", speed_factor)

            expected_movement = self.ai_cloud.speed * 0.8 * speed_factor
            self.assertEqual(self.ai_cloud.rect.y, initial_y - expected_movement)

    def test_moveWithSpeed_doesNotMoveUp_whenHitBoxTopIsLessThanNegativeFour(self):
        mock_hitbox = Mock()
        mock_hitbox.top = -5

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox_property:
            mock_hitbox_property.return_value = mock_hitbox

            initial_y = self.ai_cloud.rect.y
            speed_factor = 1.0

            self.ai_cloud._move_with_speed("up", speed_factor)

            self.assertEqual(self.ai_cloud.rect.y, initial_y)

    def test_moveWithSpeed_movesDown_whenHitBoxBottomIsLessThanHeightPlusFour(self):
        mock_hitbox = Mock()
        mock_hitbox.bottom = c.HEIGHT

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox_property:
            mock_hitbox_property.return_value = mock_hitbox

            initial_y = self.ai_cloud.rect.y
            speed_factor = 1.0

            self.ai_cloud._move_with_speed("down", speed_factor)

            expected_movement = self.ai_cloud.speed * 0.8 * speed_factor
            self.assertEqual(self.ai_cloud.rect.y, initial_y + expected_movement)

    def test_moveWithSpeed_doesNotMoveDown_whenHitBoxBottomIsGreaterThanHeightPlusFour(self):
        mock_hitbox = Mock()
        mock_hitbox.bottom = c.HEIGHT + 5

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox_property:
            mock_hitbox_property.return_value = mock_hitbox

            initial_y = self.ai_cloud.rect.y
            speed_factor = 1.0

            self.ai_cloud._move_with_speed("down", speed_factor)

            self.assertEqual(self.ai_cloud.rect.y, initial_y)