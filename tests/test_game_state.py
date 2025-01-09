from math import floor
import unittest
from unittest.mock import Mock, patch

from src.core.game_state import GameState
from src.utils import constants as c

import pygame


class GameStateShould(unittest.TestCase):
    def setUp(self):
        self.pygame_init_patch = patch("pygame.init").start()
        self.mixer_init_patch = patch("pygame.mixer.init").start()

        self.rect_mock = Mock()
        self.rect_mock.width = 64
        self.rect_mock.height = 64
        self.rect_mock.center = (0, 0)

        self.image_mock = Mock()
        self.image_mock.convert_alpha = Mock(return_value=self.image_mock)
        self.image_mock.get_rect = Mock(return_value=self.rect_mock)

        self.patches = [
            patch("pygame.image.load", return_value=self.image_mock),
            patch("pygame.transform.rotozoom", return_value=self.image_mock),
            patch("pygame.sprite.Group", return_value=Mock()),
            patch("pygame.mixer.Sound", return_value=Mock()),
            patch("pygame.mixer.music", return_value=Mock()),
        ]

        for p in self.patches:
            p.start()

        pygame.init()
        pygame.mixer.init()

        self.fox_mock = patch("src.core.game_state.Fox").start()
        self.fox_mock.return_value = Mock()

        self.cloud_mock = patch("src.core.game_state.Cloud").start()
        self.cloud_mock.return_value = Mock()

        self.ai_cloud_mock = patch("src.core.game_state.AICloud").start()
        self.ai_cloud_mock.return_value = Mock()

        self.bonus_star_mock = patch("src.core.game_state.BonusStar").start()
        self.bonus_star_mock.return_value = Mock()

        self.sound_manager_mock = patch("src.core.game_state.SoundManager").start()
        self.sound_manager_instance = Mock()
        self.sound_manager_instance.sound_muted = False
        self.sound_manager_instance.music_muted = False
        self.sound_manager_mock.return_value = self.sound_manager_instance

    def tearDown(self):
        pygame.mixer.quit()
        pygame.quit()
        patch.stopall()

    def test_init_initializesSuccessfully(self):
        game_state = GameState()

        self.assertEqual(game_state._current_state, c.GameStates.START)
        self.assertTrue(game_state.is_first_throw)
        self.assertEqual(game_state.base_speed, c.BASE_SPEED)
        self.assertEqual(game_state.current_speed, c.BASE_SPEED)
        self.assertEqual(game_state.player1_score, 0)
        self.assertEqual(game_state.player2_score, 0)
        self.assertEqual(game_state._last_player, 0)
        self.assertFalse(game_state.multiplayer)
        self.assertEqual(game_state.level, 1)
        self.assertIsInstance(game_state.all_sprites, Mock)
        self.assertIsInstance(game_state.fox, Mock)
        self.assertIsInstance(game_state.cloud_player1, Mock)
        self.assertIsInstance(game_state.cloud_player2, Mock)
        self.assertIsInstance(game_state.bonus_star, Mock)
        self.assertIsInstance(game_state.sound_manager, Mock)
        self.sound_manager_mock.assert_called_once()

    def test_update_doesNotUpdate_whenCurrentStateIsNotPlaying(self):
        game_state = GameState()
        game_state._current_state = c.GameStates.START

        game_state.update()

        self.fox_mock.update.assert_not_called()
        self.cloud_mock.update.assert_not_called()
        self.ai_cloud_mock.update.assert_not_called()

    def test_update_updates_whenCurrentStateIsPlaying(self):
        game_state = GameState()
        game_state._current_state = c.GameStates.PLAYING
        self.fox_mock.update.return_value = None
        self.cloud_mock.update.return_value = None
        self.ai_cloud_mock.update.return_value = None

        with (
            patch.object(game_state, "_check_for_winner") as mock_check_for_winner,
            patch.object(
                game_state, "_check_for_fox_cloud_collision"
            ) as mock_check_for_fox_cloud_collision,
            patch.object(
                game_state, "_check_for_bonus_star_fox_collision"
            ) as mock_check_for_bonus_star_fox_collision,
        ):
            game_state.update()

            mock_check_for_winner.assert_called_once()
            mock_check_for_fox_cloud_collision.assert_called_once()
            mock_check_for_bonus_star_fox_collision.assert_called_once()

    def test_setState_setsCurrentState(self):
        game_state = GameState()

        game_state.set_state(c.GameStates.PLAYING)

        self.assertEqual(game_state._current_state, c.GameStates.PLAYING)

    def test_checkForWinner_increasesPlayer1Score_whenWinnerIsPlayer1(self):
        game_state = GameState()

        with (
            patch.object(game_state, "_game_difficulty_update"),
            patch.object(game_state, "_play_again"),
        ):

            game_state._check_for_winner("player1")

            self.assertEqual(1, game_state.player1_score)

    def test_checkForWinner_callsGameDifficultyUpdate_whenWinnerIsPlayer1(self):
        game_state = GameState()

        with (
            patch.object(
                game_state, "_game_difficulty_update"
            ) as mock_game_difficulty_update,
            patch.object(game_state, "_play_again"),
        ):

            game_state._check_for_winner("player1")

            mock_game_difficulty_update.assert_called_once()

    def test_checkForWinner_callsPlayAgain_whenWinnerIsPlayer1(self):
        game_state = GameState()

        with (
            patch.object(game_state, "_game_difficulty_update"),
            patch.object(game_state, "_play_again") as mock_play_again,
        ):

            game_state._check_for_winner("player1")

            mock_play_again.assert_called_once()

    def test_checkForWinner_increasesPlayer2Score_whenWinnerIsPlayer2(self):
        game_state = GameState()

        with (
            patch.object(game_state, "_game_difficulty_update"),
            patch.object(game_state, "_play_again"),
        ):

            game_state._check_for_winner("player2")

            self.assertEqual(1, game_state.player2_score)

    def test_checkForWinner_callsGameDifficultyUpdate_whenWinnerIsPlayer2(self):
        game_state = GameState()

        with (
            patch.object(
                game_state, "_game_difficulty_update"
            ) as mock_game_difficulty_update,
            patch.object(game_state, "_play_again"),
        ):

            game_state._check_for_winner("player2")

            mock_game_difficulty_update.assert_called_once()

    def test_checkForWinner_callsPlayAgain_whenWinnerIsPlayer2(self):
        game_state = GameState()

        with (
            patch.object(game_state, "_game_difficulty_update"),
            patch.object(game_state, "_play_again") as mock_play_again,
        ):

            game_state._check_for_winner("player2")

            mock_play_again.assert_called_once()

    def test_gameDifficultyUpdate_returnsLevel(self):
        game_state = GameState()

        level = game_state._game_difficulty_update()

        self.assertEqual(level, game_state.level)

    def test_gameDifficultyUpdate_maintainsBaseSpeed_whenPlayersScoreIsZero(self):
        game_state = GameState()

        level = game_state._game_difficulty_update()

        self.assertEqual(game_state.current_speed, c.BASE_SPEED)
        self.assertEqual(level, floor(c.BASE_SPEED) - 5)

    def test_checkForFoxCloudCollision_handlesPlayer1Collision(self):
        game_state = GameState()
        game_state.cloud_player1.handle_fox_collision.return_value = True
        game_state.is_first_throw = False

        game_state._check_for_fox_cloud_collision()

        self.assertEqual(game_state._last_player, game_state.player1_score)
        game_state.sound_manager.play_sound.assert_called_once_with("fox-bounce")
        self.assertTrue(game_state.is_first_throw)
        game_state.fox.velocity.scale_to_length.assert_called_once_with(
            game_state.current_speed
        )

    def test_checkForFoxCloudCollision_handlesPlayer2Collision(self):
        game_state = GameState()
        game_state.cloud_player1.handle_fox_collision.return_value = False
        game_state.cloud_player2.handle_fox_collision.return_value = True
        game_state.is_first_throw = False

        game_state._check_for_fox_cloud_collision()

        self.assertEqual(game_state._last_player, game_state.player2_score)
        game_state.sound_manager.play_sound.assert_called_once_with("fox-bounce")
        self.assertTrue(game_state.is_first_throw)
        game_state.fox.velocity.scale_to_length.assert_called_once_with(
            game_state.current_speed
        )

    def test_checkForBonusStarFoxCollision_addsPointsToPlayer1_whenLastPlayerIsPlayer1(
        self,
    ):
        game_state = GameState()
        game_state.bonus_star.handle_fox_collision.return_value = 2
        game_state._last_player = game_state.player1_score
        initial_score = game_state.player1_score

        game_state._check_for_bonus_star_fox_collision()

        self.assertEqual(game_state.player1_score, initial_score + 2)
        game_state.sound_manager.play_sound.assert_called_once_with("bonus-collect")

    def test_playAgain_resetsPositionAndDespawnsStar(self):
        game_state = GameState()

        with patch.object(game_state, "_reset_fox_position") as mock_reset_position:
            game_state._play_again()

            mock_reset_position.assert_called_once()
            game_state.bonus_star.despawn.assert_called_once()

    def test_reset_resetsAllValuesToInitialState(self):
        game_state = GameState()
        game_state.player1_score = 5
        game_state.player2_score = 3
        game_state.level = 4
        game_state.current_speed = 10

        with patch.object(game_state, "_reset_fox_position") as mock_reset_position:
            game_state.reset()

            self.assertEqual(game_state.player1_score, 0)
            self.assertEqual(game_state.player2_score, 0)
            self.assertEqual(game_state.level, 1)
            self.assertEqual(game_state.current_speed, game_state.base_speed)
            mock_reset_position.assert_called_once()
            game_state.bonus_star.despawn.assert_called_once()
            game_state.cloud_player1.reset.assert_called_once()
            game_state.cloud_player2.reset.assert_called_once()
            self.assertEqual(game_state._current_state, c.GameStates.START)
