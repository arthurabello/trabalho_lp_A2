"""
Direction handling for units.
"""

from enum import IntEnum

class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @classmethod
    def to_string(cls, direction):
        """Convert direction enum to string."""
        return {
            cls.NORTH: "North",
            cls.EAST: "East", 
            cls.SOUTH: "South",
            cls.WEST: "West"
        }[direction]
    
    @classmethod
    def get_covered_directions(cls, direction):
        """Get covered directions for given direction."""
        return {
            cls.NORTH: {cls.NORTH, cls.NORTH_EAST, cls.NORTH_WEST},
            cls.EAST: {cls.EAST, cls.NORTH_EAST, cls.SOUTH_EAST},
            cls.SOUTH: {cls.SOUTH, cls.SOUTH_EAST, cls.SOUTH_WEST},
            cls.WEST: {cls.WEST, cls.NORTH_WEST, cls.SOUTH_WEST}
        }[direction]

class DirectionMixin:
    def change_direction(self, new_direction):
        """Change unit facing direction."""
        if not self.has_changed_direction:
            self.facing_direction = new_direction
            self.has_changed_direction = True
            self._update_sprite()
            return True
        return False
        
    def reset_direction_change(self):
        """Reset direction change flag."""
        self.has_changed_direction = False
        
    def _is_frontal_attack(self, attacker):
        """Determine if attack is frontal."""
        att_row, att_col = attacker.position
        def_row, def_col = self.position
        return abs(att_row - def_row) <= abs(att_col - def_col)