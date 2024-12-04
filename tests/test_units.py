import unittest
import random
from unittest.mock import MagicMock

import sys
sys.path.append("../src")

from classes.units.base.unit_direction import Direction
from classes.units.base.base_unit import BaseUnit

class TestUnitComponents(unittest.TestCase):

    def setUp(self):
        # Create a mock board and mock unit for testing
        self.board = MagicMock()
        self.board.terrain = {}
        self.board.units = []

    def test_unit_initialization(self):
        """
        Test BaseUnit initialization with valid parameters.
        Verifies correct setting of initial attributes.
        """
        unit = BaseUnit((5, 5), player=1, movement_range=3)
        
        self.assertEqual(unit.position, (5, 5))
        self.assertEqual(unit.player, 1)
        self.assertEqual(unit.movement_range, 3)
        self.assertTrue(unit.is_alive)
        self.assertEqual(unit.current_hp, unit.max_hp)
        self.assertEqual(unit.facing_direction, Direction.EAST)
        self.assertEqual(unit.formation, "Standard")

    def test_unit_initialization_invalid_parameters(self):
        """
        Test BaseUnit initialization with invalid parameters.
        Ensures proper validation of input parameters.
        """
        with self.assertRaises(ValueError):
            BaseUnit("invalid position", player=1, movement_range=3)
        
        with self.assertRaises(ValueError):
            BaseUnit((5, 5), player=3, movement_range=3)
        
        with self.assertRaises(ValueError):
            BaseUnit((5, 5), player=1, movement_range=-1)

    def test_can_move_to(self):
        """
        Test unit movement validation.
        Verifies that a unit can only move to reachable, unoccupied positions.
        """
        
        board = MagicMock()
        board.graph.get_reachable_positions.return_value = {(6, 5), (4, 5), (5, 6), (5, 4)}

        unit = BaseUnit((5, 5), player=1, movement_range=1)
        other_unit = BaseUnit((6, 5), player=2, movement_range=1)
        
        all_units = [unit, other_unit]

        self.assertTrue(unit.can_move_to((5, 6), board, all_units))
        self.assertFalse(unit.can_move_to((6, 5), board, all_units))
        self.assertFalse(unit.can_move_to((7, 5), board, all_units))

    def test_attack_direction_calculation(self):
        """
        Test _get_attack_direction method.
        Verify correct attack direction determination based on relative positioning.
        """
        defender = BaseUnit((5, 5), player=1, movement_range=3)
        defender.facing_direction = Direction.NORTH

        attacker_front = BaseUnit((6, 5), player=2, movement_range=3)
        self.assertEqual(defender._get_attack_direction(attacker_front), "front")

        attacker_rear = BaseUnit((4, 5), player=2, movement_range=3)
        self.assertEqual(defender._get_attack_direction(attacker_rear), "rear")

        attacker_flank = BaseUnit((5, 6), player=2, movement_range=3)
        self.assertEqual(defender._get_attack_direction(attacker_flank), "flank")

    def test_formation_modifier(self):
        """
        Test formation defense modifier calculations.
        Verify different modifiers for various attack and formation types.
        """

        defender = BaseUnit((5, 5), player=1, movement_range=3)
        defender.formation = "Shield Wall"
        defender.attack_type = "melee"

        melee_attacker = BaseUnit((6, 5), player=2, movement_range=3)
        melee_attacker.attack_type = "melee"

        ranged_attacker = BaseUnit((6, 5), player=2, movement_range=3)
        ranged_attacker.attack_type = "ranged"

        board = MagicMock()
        board.terrain = {(5, 5): "plains"}

        self.assertEqual(defender._get_formation_modifier(ranged_attacker), 2.5)
        self.assertEqual(defender._get_formation_modifier(melee_attacker), 1.5)

        defender.formation = "Phalanx"  
        defender._is_frontal_attack = MagicMock(return_value=True)

        self.assertEqual(defender._get_formation_modifier(melee_attacker), 3.0)

if __name__ == '__main__':
    unittest.main()