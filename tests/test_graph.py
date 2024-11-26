import unittest

import sys
sys.path.append('../src')

from classes.graph import BoardGraph

class TestBoardGraph(unittest.TestCase):
    
    def setUp(self):
        # Default configuration for testing
        terrain = {
            (0, 0): 'plains', (0, 1): 'mountain', (0, 2): 'forest',
            (1, 0): 'plains', (1, 1): 'mountain', (1, 2): 'forest',
            (2, 0): 'plains', (2, 1): 'mountain', (2, 2): 'forest'
        }
        units = [
            type('Unit', (), {'is_alive': True, 'position': (1, 1)})(),
            type('Unit', (), {'is_alive': False, 'position': (0, 0)})()
        ]
        self.graph = BoardGraph(3, 3, terrain, units)

    def test_init_valid_board(self):
        """BoardGraph startup test with valid parameters"""
        self.assertEqual(self.graph.m, 3)
        self.assertEqual(self.graph.n, 3)
        self.assertIsNotNone(self.graph.graph)

    def test_init_invalid_dimensions(self):
        """BoardGraph startup test with invalid dimensions"""
        with self.assertRaises(TypeError):
            BoardGraph('3', 3, {}, [])
        with self.assertRaises(ValueError):
            BoardGraph(0, -1, {}, [])

    def test_is_valid_position(self):
        """Test if the position the is valid in the graph"""
        self.assertTrue(self.graph._is_valid_position(0, 0))
        self.assertTrue(self.graph._is_valid_position(2, 2))
        self.assertFalse(self.graph._is_valid_position(-1, 0))
        self.assertFalse(self.graph._is_valid_position(3, 0))

    def test_calculate_edge_weight(self):
        """Testing edge weight calculation between positions"""
        self.assertEqual(self.graph._calculate_edge_weight((0, 0), (0, 1)), 2)  # plains to mountain
        self.assertEqual(self.graph._calculate_edge_weight((0, 1), (0, 0)), 1)  # mountain to plains
        self.assertEqual(self.graph._calculate_edge_weight((0, 0), (1, 0)), 1)  # plains to plains

    def test_get_neighbors(self):
        """Test getting neighbors"""
        neighbors = self.graph.get_neighbors((1, 1))
        expected_neighbor_positions = {(0, 1), (2, 1), (1, 0), (1, 2)}
        
        self.assertEqual(set(neighbors.keys()), expected_neighbor_positions)
        
    def test_get_neighbors_invalid_position(self):
        """Test getting neighbors with an invalid position"""
        with self.assertRaises(ValueError):
            self.graph.get_neighbors((-1, 0))
        with self.assertRaises(ValueError):
            self.graph.get_neighbors('invalid')

    def test_get_reachable_positions(self):
        """Test reachable positions"""
        # Reset units to test
        units = []
        reachable_positions, movement_costs = self.graph.get_reachable_positions((0, 0), 2, units)
        
        # Expected behavior
        self.assertTrue((0, 1) in reachable_positions)
        self.assertTrue((1, 0) in reachable_positions)
        self.assertFalse((2, 2) in reachable_positions)
        
        # Movement costs
        self.assertIn((0, 0), movement_costs)
        self.assertTrue(movement_costs[(0, 0)] == 0)

    def test_get_reachable_positions_invalid_parameters(self):
        """Test reachable positions with invalid parameters"""
        with self.assertRaises(ValueError):
            self.graph.get_reachable_positions((10, 10), 2, [])
        
        with self.assertRaises(TypeError):
            self.graph.get_reachable_positions((0, 0), '2', [])

    def test_update_units(self):
        """Test updating units"""
        new_units = [
            type('Unit', (), {'is_alive': True, 'position': (2, 2)})()
        ]
        
        # get the neighbors before updating units
        original_neighbors = self.graph.get_neighbors((2, 1))
        original_neighbor_weight = original_neighbors.get((2, 2), 0)
        self.assertNotEqual(original_neighbor_weight, float('infinity'))

        self.graph.update_units(new_units)

        # get the neighbors after updating units
        updated_neighbors = self.graph.get_neighbors((2, 1))
        neighbor_weight = updated_neighbors.get((2, 2), 0)
        self.assertEqual(neighbor_weight, float('infinity'))

if __name__ == '__main__':
    unittest.main()