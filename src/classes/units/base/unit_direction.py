"""
Direction handling for units.
"""

from enum import IntEnum

class Direction(IntEnum):
    """
    Enum representing the four cardinal directions (North, East, South, West).
    
    This class is used to handle direction-related functionality for units.
    """
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @classmethod
    def to_string(cls, direction):
        """
        Converts a direction enum value to a string representation.
        
        Args:
            direction (Direction): The direction enum value to be converted.

        Returns:
            str: The string representation of the direction (e.g., "North", "East").
        """
        return {
            cls.NORTH: "North",
            cls.EAST: "East", 
            cls.SOUTH: "South",
            cls.WEST: "West"
        }[direction]
    
    @classmethod
    def get_covered_directions(cls, direction):
        """
        Returns the set of directions covered by a given direction.
        
        Args:
            direction (Direction): The direction for which to find the covered directions.
        
        Returns:
            set: A set of directions covered by the given direction (e.g., North-East, South-West).
        """
        return {
            cls.NORTH: {cls.NORTH, cls.NORTH_EAST, cls.NORTH_WEST},
            cls.EAST: {cls.EAST, cls.NORTH_EAST, cls.SOUTH_EAST},
            cls.SOUTH: {cls.SOUTH, cls.SOUTH_EAST, cls.SOUTH_WEST},
            cls.WEST: {cls.WEST, cls.NORTH_WEST, cls.SOUTH_WEST}
        }[direction]

class DirectionMixin:
    """
    Mixin class providing direction-related methods for units.
    
    This class adds methods to handle unit direction changes, reset direction status,
    and check if an attack is frontal.
    """
    def change_direction(self, new_direction):
        """
        Changes the unit's facing direction if it hasn't changed already.
        
        Args:
            new_direction (Direction): The new direction the unit should face.
        
        Returns:
            bool: True if the direction was successfully changed, False if the direction 
                  has already been changed.
        """
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
        """
        Determines whether an attack is coming from the front of the unit.
        
        Args:
            attacker (BaseUnit): The unit that is attacking.
        
        Returns:
            bool: True if the attack is frontal (i.e., the attacker's row is aligned with 
                  the defender's row), False otherwise.
        """
        att_row, att_col = attacker.position
        def_row, def_col = self.position
        return abs(att_row - def_row) <= abs(att_col - def_col)