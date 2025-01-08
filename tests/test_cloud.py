import unittest
from unittest.mock import Mock, patch, PropertyMock, MagicMock

import pygame

from src.core.cloud import Cloud
from src.utils import constants as c


class CloudShould(unittest.TestCase):
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

        self.cloud = Cloud("player1")

    def test_init_initializesSuccessfully(self):
        self.assertIsNotNone(self.cloud)

    def test_init_setsSpeed(self):
        self.assertEqual(c.BASE_SPEED * 0.35, self.cloud.speed)

    def test_init_setsCollisionCooldown(self):
        self.assertEqual(0, self.cloud.collision_cooldown)

    def test_init_setsShakeDuration(self):
        self.assertEqual(20, self.cloud.shake_duration)

    def test_init_setsShakeIntensity(self):
        self.assertEqual(1, self.cloud.shake_intensity)

    def test_init_setsIsShaking(self):
        self.assertFalse(self.cloud.is_shaking)

    def test_init_setsShakeStart(self):
        self.assertEqual(0, self.cloud.shake_start)

    def test_init_setsOriginalPos(self):
        self.assertIsNone(self.cloud.original_pos)

    def test_init_setsPosition(self):
        self.assertEqual("player1", self.cloud.player)

    def test_init_setsImage(self):
        self.assertIsNotNone(self.cloud.image)

    def test_init_setsRect(self):
        self.assertIsNotNone(self.cloud.rect)

    def test_hitbox_returnsCorrectHitbox(self):
        mock_rect = Mock()
        mock_rect.width = 100
        mock_rect.height = 80
        mock_rect.center = (50, 40)
        mock_rect.left = 0

        mock_copy = Mock()
        mock_rect.copy.return_value = mock_copy

        self.cloud.rect = mock_rect
        self.cloud.player = "player1"

        _ = self.cloud.hitbox
        mock_rect.copy.assert_called_once()

        self.assertEqual(mock_rect.width - c.CLOUD_HITBOX_WIDTH_DIFF, mock_copy.width)
        self.assertEqual(mock_rect.height + c.CLOUD_HITBOX_HEIGHT_DIFF, mock_copy.height)
        self.assertEqual(mock_rect.left, mock_copy.left)

    def test_update_callsUpdateShake(self):
        with (patch.object(self.cloud, 'update_shake') as mock_update_shake,
              patch('pygame.key.get_pressed'),
              patch.object(self.cloud, 'move')):
            self.cloud.update(Mock())
            mock_update_shake.assert_called_once()

    def test_update_movesCloudUp(self):
        self.cloud.player = "player1"
        self.cloud.move = Mock()

        keys = [0] * 500
        keys[pygame.K_w] = 1

        with (patch.object(self.cloud, 'update_shake'),
              patch('pygame.key.get_pressed', return_value=keys)):
            self.cloud.update(Mock())

        self.cloud.move.assert_called_once_with("up")

    def test_update_movesCloudDown(self):
        self.cloud.player = "player1"
        self.cloud.move = Mock()

        keys = [0] * 500
        keys[pygame.K_s] = 1

        with (patch.object(self.cloud, 'update_shake'),
              patch('pygame.key.get_pressed', return_value=keys)):
            self.cloud.update(Mock())

        self.cloud.move.assert_called_once_with("down")

    def test_setPosition_setsPositionForPlayer1(self):
        self.cloud._set_position("player1")
        self.assertEqual(c.CLOUD_PLAYER1_X, self.cloud.rect.x)
        self.assertEqual(c.CLOUD_Y, self.cloud.rect.y)

    def test_setPosition_setsPositionForPlayer2(self):
        self.cloud._set_position("player2")
        self.assertEqual(c.CLOUD_PLAYER2_X, self.cloud.rect.x)
        self.assertEqual(c.CLOUD_Y, self.cloud.rect.y)

    def test_move_movesCloudUp_whenDirectionIsUp(self):
        mock_rect = MagicMock()
        mock_rect.y = 100

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            mock_hitbox.return_value = MagicMock()
            mock_hitbox.return_value.top = 10
            self.cloud.rect = mock_rect

            self.cloud.move("up")

            self.assertEqual(self.cloud.rect.y, 100 - self.cloud.speed)

    def test_move_movesCloudDown_whenDirectionIsDown(self):
        mock_rect = MagicMock()
        mock_rect.y = 100

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            mock_hitbox.return_value = MagicMock()
            mock_hitbox.return_value.bottom = 200
            self.cloud.rect = mock_rect

            self.cloud.move("down")

            self.assertEqual(self.cloud.rect.y, 100 + self.cloud.speed)

    def test_handleFoxCollision_returnsFalse_whenFoxDoesNotCollideWithCloud(self):
        fox = Mock()
        fox.hitbox.colliderect.return_value = False

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock):

            self.assertFalse(self.cloud.handle_fox_collision(fox))

    def test_handleFoxCollision_callsInitCollisionState_whenFoxCollidesWithCloud(self):
        fox = Mock()
        fox.hitbox.colliderect.return_value = True

        with (patch.object(self.cloud, '_init_collision_state') as mock_init_collision_state,
              patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock),
              patch.object(self.cloud, '_calculate_overlaps', return_value=(10, 20)),
              patch.object(self.cloud, '_handle_side_collision'),
              ):
            self.cloud.handle_fox_collision(fox)

            mock_init_collision_state.assert_called_once()

    def test_handleFoxCollision_callsHandleSideCollision_whenOverlapXLessThanOverlapY(self):
        fox = Mock()
        fox.hitbox.colliderect.return_value = True

        with (patch.object(self.cloud, '_init_collision_state'),
              patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock),
              patch.object(self.cloud, '_calculate_overlaps', return_value=(10, 20)),
              patch.object(self.cloud, '_handle_side_collision') as mock_handle_side_collision,
              ):
            self.cloud.handle_fox_collision(fox)

            mock_handle_side_collision.assert_called_once()

    def test_handleFoxCollision_callsHandleVerticalCollision_whenOverlapXGreaterThanOverlapY(self):
        fox = Mock()
        fox.hitbox.colliderect.return_value = True

        with (patch.object(self.cloud, '_init_collision_state'),
              patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock),
              patch.object(self.cloud, '_calculate_overlaps', return_value=(20, 10)),
              patch.object(self.cloud, '_handle_vertical_collision') as mock_handle_vertical_collision,
              ):
            self.cloud.handle_fox_collision(fox)

            mock_handle_vertical_collision.assert_called_once()

    def test_handleFoxCollision_returnsTrue_whenFoxCollidesWithCloud(self):
        fox = Mock()
        fox.hitbox.colliderect.return_value = True

        with (patch.object(self.cloud, '_init_collision_state'),
              patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock),
              patch.object(self.cloud, '_calculate_overlaps', return_value=(20, 10)),
              patch.object(self.cloud, '_handle_vertical_collision'),
              ):
            self.assertTrue(self.cloud.handle_fox_collision(fox))

    def test_initCollisionState_setsIsShakingToTrue(self):
        self.cloud.is_shaking = False
        self.cloud._init_collision_state()
        self.assertTrue(self.cloud.is_shaking)

    def test_initCollisionState_setsShakeStartToCurrentTime(self):
        self.cloud.shake_start = 0
        self.cloud._init_collision_state()
        self.assertEqual(pygame.time.get_ticks(), self.cloud.shake_start)

    def test_initCollisionState_setsOriginalPosToCurrentRect(self):
        mock_rect = MagicMock()
        mock_rect.copy.return_value = mock_rect
        self.cloud.rect = mock_rect

        self.cloud._init_collision_state()

        mock_rect.copy.assert_called_once()
        self.assertIsNotNone(self.cloud.original_pos)

    def test_calculateOverlaps_returnsCorrectOverlaps(self):
        fox = Mock()
        fox.hitbox.right = 100
        fox.hitbox.left = 50
        fox.hitbox.bottom = 200
        fox.hitbox.top = 150

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            mock_hitbox.return_value = MagicMock()
            mock_hitbox.return_value.left = 75
            mock_hitbox.return_value.right = 125
            mock_hitbox.return_value.top = 175
            mock_hitbox.return_value.bottom = 225

            overlap_x, overlap_y = self.cloud._calculate_overlaps(fox)

            self.assertEqual(25, overlap_x)
            self.assertEqual(25, overlap_y)

    def test_handleSideCollision_callsApplySideBounce_whenValidSideHit(self):
        fox = Mock()
        fox.velocity = Mock()
        fox.velocity.length.return_value = 10

        with patch.object(self.cloud, '_is_valid_side_hit', return_value=True), \
                patch.object(self.cloud, '_apply_side_bounce') as mock_apply_side_bounce:
            self.cloud._handle_side_collision(fox)

            mock_apply_side_bounce.assert_called_once()

    def test_handleSideCollision_callsFixInvalidSideHit_whenInvalidSideHit(self):
        fox = Mock()
        fox.velocity = Mock()
        fox.velocity.length.return_value = 10

        with patch.object(self.cloud, '_is_valid_side_hit', return_value=False), \
                patch.object(self.cloud, '_fix_invalid_side_hit') as mock_fix_invalid_side_hit:
            self.cloud._handle_side_collision(fox)

            mock_fix_invalid_side_hit.assert_called_once()

    def test_isValidSideHit_returnsTrue_whenPlayer1AndFoxIsToRight(self):
        fox = Mock()
        fox.hitbox.centerx = 100
        self.cloud.player = "player1"

        mock_rect = MagicMock()
        mock_rect.width = 100
        self.cloud.rect = mock_rect

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            type(mock_hitbox.return_value).centerx = PropertyMock(return_value=50)

            result = self.cloud._is_valid_side_hit(fox)
            self.assertTrue(result)

    def test_isValidSideHit_returnsFalse_whenPlayer1AndFoxIsToLeft(self):
        fox = Mock()
        fox.hitbox.centerx = 50
        self.cloud.player = "player1"

        mock_rect = MagicMock()
        mock_rect.width = 100
        self.cloud.rect = mock_rect

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            type(mock_hitbox.return_value).centerx = PropertyMock(return_value=100)

            result = self.cloud._is_valid_side_hit(fox)
            self.assertFalse(result)

    def test_isValidSideHit_returnsTrue_whenPlayer2AndFoxIsToLeft(self):
        fox = Mock()
        fox.hitbox.centerx = 50
        self.cloud.player = "player2"

        mock_rect = MagicMock()
        mock_rect.width = 100
        self.cloud.rect = mock_rect

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            type(mock_hitbox.return_value).centerx = PropertyMock(return_value=100)

            result = self.cloud._is_valid_side_hit(fox)
            self.assertTrue(result)

    def test_isValidSideHit_returnsFalse_whenPlayer2AndFoxIsToRight(self):
        fox = Mock()
        fox.hitbox.centerx = 100
        self.cloud.player = "player2"

        mock_rect = MagicMock()
        mock_rect.width = 100
        self.cloud.rect = mock_rect

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            type(mock_hitbox.return_value).centerx = PropertyMock(return_value=50)

            result = self.cloud._is_valid_side_hit(fox)
            self.assertFalse(result)

    def test_applySideBounce_setsPositiveVelocityX_whenPlayer1(self):
        self.cloud.player = "player1"
        fox = MagicMock()
        fox.velocity.x = -5
        fox.velocity.length.return_value = 10

        with patch.object(self.cloud, '_calculate_vertical_bounce', return_value=3):
            # Act
            self.cloud._apply_side_bounce(fox)

            self.assertEqual(5, fox.velocity.x)  # трябва да е станало положително
            self.assertEqual(3, fox.velocity.y)  # трябва да е равно на vertical_bounce
            fox.velocity.scale_to_length.assert_called_once_with(10)

    def test_applySideBounce_setsNegativeVelocityX_whenPlayer2(self):
        self.cloud.player = "player2"
        fox = MagicMock()
        fox.velocity.x = 5
        fox.velocity.length.return_value = 10

        with patch.object(self.cloud, '_calculate_vertical_bounce', return_value=3):
            self.cloud._apply_side_bounce(fox)

            self.assertEqual(-5, fox.velocity.x)
            self.assertEqual(3, fox.velocity.y)
            fox.velocity.scale_to_length.assert_called_once_with(10)

    def test_applySideBounce_scalesVelocityToOriginalLength(self):
        self.cloud.player = "player1"
        fox = MagicMock()
        fox.velocity.x = 3
        fox.velocity.length.return_value = 5

        with patch.object(self.cloud, '_calculate_vertical_bounce', return_value=4):
            self.cloud._apply_side_bounce(fox)

            fox.velocity.length.assert_called_once()
            fox.velocity.scale_to_length.assert_called_once_with(5)

    def test_applySideBounce_usesCalculatedVerticalBounce(self):
        self.cloud.player = "player1"
        fox = MagicMock()
        expected_bounce = 2.5

        with patch.object(self.cloud, '_calculate_vertical_bounce', return_value=expected_bounce) as mock_calc:
            self.cloud._apply_side_bounce(fox)

            mock_calc.assert_called_once_with(fox)
            self.assertEqual(expected_bounce, fox.velocity.y)

    def test_calculateVerticalBounce_calculatesCorrectBounce_whenAboveMinimum(self):
        # Arrange
        fox = MagicMock()
        fox.hitbox.centery = 150

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            type(mock_hitbox.return_value).centery = PropertyMock(return_value=100)
            type(mock_hitbox.return_value).height = PropertyMock(return_value=40)

            result = self.cloud._calculate_vertical_bounce(fox)

            expected_bounce = 2.5 * c.BASE_SPEED
            self.assertEqual(expected_bounce, result)

    def test_calculateVerticalBounce_calculatesCorrectBounce_whenBelowMinimum(self):
        fox = MagicMock()
        fox.hitbox.centery = 105

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            type(mock_hitbox.return_value).centery = PropertyMock(return_value=100)
            type(mock_hitbox.return_value).height = PropertyMock(return_value=40)

            result = self.cloud._calculate_vertical_bounce(fox)

            expected_bounce = 0.3 * c.BASE_SPEED
            self.assertEqual(expected_bounce, result)

    def test_calculateVerticalBounce_returnsNegativeMinimum_whenBelowMinimumAndNegative(self):
        # Arrange
        fox = MagicMock()
        fox.hitbox.centery = 95

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            type(mock_hitbox.return_value).centery = PropertyMock(return_value=100)
            type(mock_hitbox.return_value).height = PropertyMock(return_value=40)

            result = self.cloud._calculate_vertical_bounce(fox)

            expected_bounce = -0.3 * c.BASE_SPEED
            self.assertEqual(expected_bounce, result)

    def test_calculateVerticalBounce_calculatesCorrectBounce_whenNegativeAndAboveMinimum(self):
        fox = MagicMock()
        fox.hitbox.centery = 50

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            type(mock_hitbox.return_value).centery = PropertyMock(return_value=100)
            type(mock_hitbox.return_value).height = PropertyMock(return_value=40)

            result = self.cloud._calculate_vertical_bounce(fox)

            expected_bounce = -2.5 * c.BASE_SPEED
            self.assertEqual(expected_bounce, result)

    def test_fixInvalidSideHit_setsPositiveVelocityX_whenPlayer1AndFoxRight(self):
        self.cloud.player = "player1"
        fox = MagicMock()
        fox.velocity.x = -5

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            type(mock_hitbox.return_value).centerx = PropertyMock(return_value=50)
            fox.hitbox.centerx = 100

            self.cloud._fix_invalid_side_hit(fox)

            self.assertEqual(5, fox.velocity.x)

    def test_fixInvalidSideHit_setsNegativeVelocityX_whenPlayer2AndFoxLeft(self):
        self.cloud.player = "player2"
        fox = MagicMock()
        fox.velocity.x = 5

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            type(mock_hitbox.return_value).centerx = PropertyMock(return_value=100)
            fox.hitbox.centerx = 50

            self.cloud._fix_invalid_side_hit(fox)

            self.assertEqual(-5, fox.velocity.x)

    def test_handleVerticalCollision_setsFoxPositionAndVelocity_whenHitFromTop(self):
        fox = MagicMock()
        fox.hitbox.centery = 50
        fox.velocity.y = 5

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            type(mock_hitbox.return_value).centery = PropertyMock(return_value=100)
            type(mock_hitbox.return_value).top = PropertyMock(return_value=80)

            self.cloud._handle_vertical_collision(fox)

            expected_bottom = 80 - c.FOX_HITBOX_DIFF * 0.75
            self.assertEqual(expected_bottom, fox.rect.bottom)
            self.assertEqual(-5, fox.velocity.y)
            self.assertEqual(3, self.cloud.collision_cooldown)

    def test_handleVerticalCollision_setsFoxPositionAndVelocity_whenHitFromBottom(self):
        fox = MagicMock()
        fox.hitbox.centery = 150
        fox.velocity.y = -5

        with patch('src.core.cloud.Cloud.hitbox', new_callable=PropertyMock) as mock_hitbox:
            type(mock_hitbox.return_value).centery = PropertyMock(return_value=100)
            type(mock_hitbox.return_value).bottom = PropertyMock(return_value=120)

            self.cloud._handle_vertical_collision(fox)

            expected_top = 120 + c.FOX_HITBOX_DIFF * 0.75
            self.assertEqual(expected_top, fox.rect.top)
            self.assertEqual(5, fox.velocity.y)
            self.assertEqual(3, self.cloud.collision_cooldown)

    def test_reset_resetsPositionAndCooldown(self):
        self.cloud.collision_cooldown = 5
        mock_set_position = MagicMock()
        self.cloud._set_position = mock_set_position

        self.cloud.reset()

        mock_set_position.assert_called_once_with(self.cloud.player)
        self.assertEqual(0, self.cloud.collision_cooldown)

    def test_updateShake_stopsShakingAfterDuration(self):
        self.cloud.is_shaking = True
        self.cloud.shake_start = pygame.time.get_ticks() - self.cloud.shake_duration - 1
        self.cloud.original_pos = MagicMock()
        self.cloud.original_pos.center = (100, 100)

        self.cloud.update_shake()

        self.assertFalse(self.cloud.is_shaking)
        self.assertEqual(self.cloud.original_pos.center, self.cloud.rect.center)

    @patch('random.randint')
    def test_updateShake_appliesRandomOffset(self, mock_randint):
        self.cloud.is_shaking = True
        self.cloud.shake_start = pygame.time.get_ticks()
        self.cloud.original_pos = MagicMock()
        self.cloud.original_pos.centerx = 100
        self.cloud.original_pos.centery = 100
        mock_randint.side_effect = [2, -3]  # За x и y offset

        self.cloud.update_shake()

        self.assertEqual(102, self.cloud.rect.centerx)
        self.assertEqual(97, self.cloud.rect.centery)
        self.assertEqual(2, mock_randint.call_count)
