import unittest
from unittest.mock import MagicMock

import sys
sys.path.append('../src')

from classes.game.core.combat_manager import CombatManager

class TestCombatManager(unittest.TestCase):
    """
    Unit tests for the CombatManager class.
    """
    def setUp(self):
        """Set up test environment."""
        self.state_manager = MagicMock()  # Mock the state manager
        self.state_manager.board = MagicMock()  # Mock the game board
        self.state_manager.current_player = 1
        self.state_manager.game_over = False
        self.state_manager.winner = None
        self.combat_manager = CombatManager(self.state_manager)

        # Mock units
        self.attacker = MagicMock()
        self.defender = MagicMock()
        self.attacker.is_alive = True
        self.attacker.has_attacked = False
        self.attacker.player = 1
        self.attacker.has_general = False
        self.defender.is_alive = True
        self.defender.player = 2
        self.defender.has_general = False

    def test_handle_combat_success(self):
        """
        Test successful combat interaction.
        """
        self.combat_manager._validate_combat = MagicMock(return_value=True)
        self.attacker.attack = MagicMock()

        result = self.combat_manager.handle_combat(self.attacker, self.defender)
        self.attacker.attack.assert_called_once_with(self.defender, self.state_manager.board)
        self.assertTrue(result)
        self.assertFalse(self.state_manager.game_over)

    def test_handle_combat_defender_general_dies(self):
        """
        Test game-over condition when defender's general dies.
        """
        self.combat_manager._validate_combat = MagicMock(return_value=True)
        self.defender.has_general = True
        self.defender.is_alive = False

        result = self.combat_manager.handle_combat(self.attacker, self.defender)
        self.assertTrue(self.state_manager.game_over)
        self.assertEqual(self.state_manager.winner, 1)
        self.assertTrue(result)

    def test_handle_combat_attacker_general_dies(self):
        """
        Test game-over condition when attacker's general dies.
        """
        self.combat_manager._validate_combat = MagicMock(return_value=True)
        self.attacker.has_general = True
        self.attacker.is_alive = False

        result = self.combat_manager.handle_combat(self.attacker, self.defender)
        self.assertTrue(self.state_manager.game_over)
        self.assertEqual(self.state_manager.winner, 2)
        self.assertTrue(result)

    def test_handle_combat_invalid(self):
        """
        Test combat with invalid conditions.
        """
        self.combat_manager._validate_combat = MagicMock(return_value=False)
        result = self.combat_manager.handle_combat(self.attacker, self.defender)
        self.assertFalse(result)

    def test_validate_combat_dead_attacker(self):
        """
        Test validation failure when the attacker is dead.
        """
        self.attacker.is_alive = False
        result = self.combat_manager._validate_combat(self.attacker, self.defender)
        self.assertFalse(result)

    def test_validate_combat_same_player(self):
        """
        Test validation failure when both units belong to the same player.
        """
        self.defender.player = self.attacker.player
        result = self.combat_manager._validate_combat(self.attacker, self.defender)
        self.assertFalse(result)

    def test_validate_combat_attacker_already_attacked(self):
        """
        Test validation failure when the attacker has already attacked.
        """
        self.attacker.has_attacked = True
        result = self.combat_manager._validate_combat(self.attacker, self.defender)
        self.assertFalse(result)

    def test_check_game_over_no_generals(self):
        """
        Test game-over condition when no generals are alive.
        """
        self.state_manager.units1 = [MagicMock(is_alive=False, has_general=True)]
        self.state_manager.units2 = [MagicMock(is_alive=False, has_general=True)]

        self.combat_manager.check_game_over()
        self.assertTrue(self.state_manager.game_over)
        self.assertEqual(self.state_manager.winner, 2)  # Assuming player 2 wins in this case.

    def test_check_game_over_generals_alive(self):
        """
        Test no game-over condition when generals are alive.
        """
        self.state_manager.units1 = [MagicMock(is_alive=True, has_general=True)]
        self.state_manager.units2 = [MagicMock(is_alive=True, has_general=True)]

        self.combat_manager.check_game_over()
        self.assertFalse(self.state_manager.game_over)

if __name__ == "__main__":
    unittest.main()