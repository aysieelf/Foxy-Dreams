import unittest
from unittest.mock import Mock, PropertyMock, patch

from src.core.bonus_star import BonusStar
from src.utils import constants as c


class BonusStarShould(unittest.TestCase):
    @patch("pygame.transform.rotozoom")
    @patch("pygame.image.load")
    def setUp(self, mock_load, mock_rotozoom):
        mock_surface = Mock()
        mock_converted_surface = Mock()
        mock_rotated_surface = Mock()

        mock_surface.convert_alpha.return_value = mock_converted_surface
        mock_load.return_value = mock_surface
        mock_rotozoom.return_value = mock_rotated_surface

        mock_rotated_surface.get_rect.return_value = Mock()

        mock_sprite_group = Mock()
        mock_game_state = Mock()
        self.bonus_star = BonusStar(mock_sprite_group, mock_game_state)

    def test_init_initializesSuccessfully(self):
        self.assertIsNotNone(self.bonus_star)

    def test_init_setsActiveToFalse(self):
        self.assertFalse(self.bonus_star._active)

    def test_init_setsSpriteGroup(self):
        self.assertIsNotNone(self.bonus_star.sprite_group)

    def test_init_setsCollisionCooldownToZero(self):
        self.assertEqual(0, self.bonus_star.collision_cooldown)

    def test_init_setsParticleSystem(self):
        self.assertIsNotNone(self.bonus_star.particle_system)

    def test_init_setsImage(self):
        self.assertIsNotNone(self.bonus_star.image)

    def test_init_setsRect(self):
        self.assertIsNotNone(self.bonus_star.rect)

    def test_hitbox_returnsRectWithAdjustedWidthAndHeight(self):
        self.bonus_star.rect.width = 100
        self.bonus_star.rect.height = 100
        self.bonus_star.rect.center = (0, 0)

        hitbox = self.bonus_star.hitbox

        self.assertEqual(100 - c.BONUS_HITBOX_DIFF, hitbox.width)
        self.assertEqual(100 - c.BONUS_HITBOX_DIFF, hitbox.height)
        self.assertEqual((0, 0), hitbox.center)

    def test_spawn_doesNotAddToSpriteGroupWhenGameStateIsNotPlaying(self):
        self.bonus_star.game_state.current_state = c.GameStates.START

        self.bonus_star.spawn()

        self.assertFalse(self.bonus_star.sprite_group.add.called)

    def test_spawn_setsActiveToTrue(self):
        with patch.object(self.bonus_star, "_set_pos"), patch("pygame.time.set_timer"):

            self.bonus_star.game_state.current_state = c.GameStates.PLAYING

            self.bonus_star.spawn()

            self.assertTrue(self.bonus_star._active)

    def test_spawn_setsPosition(self):
        with (
            patch.object(self.bonus_star, "_set_pos") as mock_set_pos,
            patch("pygame.time.set_timer"),
        ):
            self.bonus_star.game_state.current_state = c.GameStates.PLAYING

            self.bonus_star.spawn()

            mock_set_pos.assert_called_once()

    def test_spawn_addsToSpriteGroup(self):
        with patch.object(self.bonus_star, "_set_pos"), patch("pygame.time.set_timer"):

            self.bonus_star.game_state.current_state = c.GameStates.PLAYING

            self.bonus_star.spawn()

            self.assertTrue(self.bonus_star.sprite_group.add.called)

    def test_spawn_setsTimer(self):
        with (
            patch.object(self.bonus_star, "_set_pos"),
            patch("pygame.time.set_timer") as mock_set_timer,
        ):

            self.bonus_star.game_state.current_state = c.GameStates.PLAYING

            self.bonus_star.spawn()

            mock_set_timer.assert_called_once_with(
                c.BONUS_DE_SPAWN_EVENT, c.BONUS_LIFETIME
            )

    def test_despawn_doesNotRemoveFromSpriteGroupWhenGameStateIsNotPlaying(self):
        self.bonus_star.game_state.current_state = c.GameStates.START

        self.bonus_star.despawn()

        self.assertFalse(self.bonus_star.sprite_group.remove.called)

    def test_despawn_setsActiveToFalse(self):
        with patch("pygame.time.set_timer"):
            self.bonus_star.game_state.current_state = c.GameStates.PLAYING

            self.bonus_star.despawn()

            self.assertFalse(self.bonus_star._active)

    def test_despawn_removesFromSpriteGroup(self):
        with patch("pygame.time.set_timer"):
            self.bonus_star.game_state.current_state = c.GameStates.PLAYING

            self.bonus_star.despawn()

            self.assertTrue(self.bonus_star.sprite_group.remove.called)

    def test_despawn_resetsCollisionCooldown(self):
        with patch("pygame.time.set_timer"):
            self.bonus_star.game_state.current_state = c.GameStates.PLAYING

            self.bonus_star.despawn()

            self.assertEqual(0, self.bonus_star.collision_cooldown)

    def test_despawn_setsTimer(self):
        with patch("pygame.time.set_timer") as mock_set_timer:
            self.bonus_star.game_state.current_state = c.GameStates.PLAYING

            self.bonus_star.despawn()

            mock_set_timer.assert_called_once_with(c.BONUS_DE_SPAWN_EVENT, 0)

    def test_setPos_setsRectCenterToRandomPosition(self):
        with patch(
            "src.core.bonus_star.get_random_position"
        ) as mock_get_random_position:
            self.bonus_star._set_pos()

            mock_get_random_position.assert_called_once()

            self.assertEqual(
                mock_get_random_position.return_value, self.bonus_star.rect.center
            )

    def test_handleFoxCollision_returnsZeroWhenNotActive(self):
        self.bonus_star._active = False

        result = self.bonus_star.handle_fox_collision(Mock())

        self.assertEqual(0, result)

    def test_handleFoxCollision_returnsZeroWhenCollisionCooldownGreaterThanZero(self):
        self.bonus_star.collision_cooldown = 1

        result = self.bonus_star.handle_fox_collision(Mock())

        self.assertEqual(0, result)

    def test_handleFoxCollision_returnsBonusPoints_whenFoxCollidesWithHitbox(self):
        self.bonus_star._active = True
        self.bonus_star.collision_cooldown = 0

        fox = Mock()
        fox.hitbox = Mock()
        fox.hitbox.colliderect.return_value = True

        mock_rect = Mock()
        mock_rect.center = (100, 100)
        self.bonus_star.rect = mock_rect

        with (
            patch.object(BonusStar, "hitbox", new_callable=PropertyMock),
            patch.object(self.bonus_star, "particle_system"),
            patch.object(self.bonus_star, "despawn"),
        ):

            result = self.bonus_star.handle_fox_collision(fox)

            self.assertEqual(c.BONUS_POINTS, result)

    def test_handleFoxCollision_returnsZero_whenFoxDoesNotColliedWithHitbox(self):
        self.bonus_star._active = True
        self.bonus_star.collision_cooldown = 0

        fox = Mock()
        fox.hitbox = Mock()
        fox.hitbox.colliderect.return_value = False

        mock_rect = Mock()
        mock_rect.center = (100, 100)
        self.bonus_star.rect = mock_rect

        with (
            patch.object(BonusStar, "hitbox", new_callable=PropertyMock),
            patch.object(self.bonus_star, "particle_system"),
            patch.object(self.bonus_star, "despawn"),
        ):

            result = self.bonus_star.handle_fox_collision(fox)

            self.assertEqual(0, result)
