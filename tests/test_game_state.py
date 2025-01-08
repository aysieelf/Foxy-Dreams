import unittest
from unittest.mock import Mock

from src.core.game_state import GameState
from src.utils import constants as c


class GameStateShould(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()

    def test_init_initializesSuccessfully(self):
        self.assertIsNotNone(self.game_state)

    def test_init_setsCurrentState(self):
        self.assertEqual(c.GameStates.START, self.game_state._current_state)

    def test_init_setsIsFirstThrow(self):
        self.assertTrue(self.game_state.is_first_throw)

    def test_init_setsBaseSpeed(self):
        self.assertEqual(c.BASE_SPEED, self.game_state.base_speed)

    def test_init_setsCurrentSpeed(self):
        self.assertEqual(c.BASE_SPEED, self.game_state.current_speed)

    def test_init_setsPlayer1Score(self):
        self.assertEqual(0, self.game_state.player1_score)

    def test_init_setsPlayer2Score(self):
        self.assertEqual(0, self.game_state.player2_score)

    def test_init_setsLastPlayer(self):
        self.assertEqual(0, self.game_state._last_player)

    def test_init_setsMultiplayer(self):
        self.assertFalse(self.game_state.multiplayer)

    def test_init_setsLevel(self):
        self.assertEqual(1, self.game_state.level)

    def test_init_setsAllSprites(self):
        self.assertIsNotNone(self.game_state.all_sprites)

    def test_init_setsFox(self):
        self.assertIsNotNone(self.game_state.fox)

    def test_init_setsCloudPlayer1(self):
        self.assertIsNotNone(self.game_state.cloud_player1)

    def test_init_setsCloudPlayer2(self):
        self.assertIsNotNone(self.game_state.cloud_player2)

    def test_init_setsBonusStar(self):
        self.assertIsNotNone(self.game_state.bonus_star)

    def test_init_addsFoxToAllSprites(self):
        self.assertIn(self.game_state.fox, self.game_state.all_sprites)

    def test_init_addsCloudPlayer1ToAllSprites(self):
        self.assertIn(self.game_state.cloud_player1, self.game_state.all_sprites)

    def test_init_addsCloudPlayer2ToAllSprites(self):
        self.assertIn(self.game_state.cloud_player2, self.game_state.all_sprites)

    def test_init_addsBonusStarToAllSprites(self):
        self.assertIn(self.game_state.bonus_star, self.game_state.all_sprites)

    def test_init_setsSoundManager(self):
        self.assertIsNotNone(self.game_state.sound_manager)

    def test_init_startsMusic(self):
        self.game_state.sound_manager.start_music.assert_called_once()


