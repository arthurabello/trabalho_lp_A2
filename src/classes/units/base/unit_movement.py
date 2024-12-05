"""
Movement-related functionality for units.
"""

class UnitMovementMixin:
    """
    Mixin class providing movement-related functionality for units.
    """
    def move(self, new_position):
        """
        Moves the unit to a new position.

        This method updates the unit's position and plays a sound effect associated 
        with movement. The unit must be alive to move.

        Args:
            new_position (tuple): The new position to which the unit will be moved, 
                                   represented as a tuple (row, col).
        """
        if not self.is_alive:
            return

        self.position = new_position
        self._play_move_sound()

    def can_move_to(self, position, board, all_units):
        """
        Checks if the unit can move to the specified position.

        This method checks if the target position is within the unit's movement range, 
        and whether the position is occupied by another unit. The unit must be alive 
        and the position must be reachable on the board.

        Args:
            position (tuple): The target position to check, represented as a tuple (row, col).
            board (GameBoard): The game board containing the unit and terrain data.
            all_units (list): A list of all units in the game to check for potential collisions.

        Returns:
            bool: True if the unit can move to the position, False otherwise.
        """
        if not self.is_alive:
            return False

        reachable = board.graph.get_reachable_positions(
            self.position, 
            self.movement_range
        )
        if position not in reachable:
            return False

        for unit in all_units:
            if (unit != self and unit.is_alive and 
                unit.position == position):
                return False

        return True

    def _play_move_sound(self):
        """Play movement sound effect."""
        try:
            self.move_sound.play()
        except Exception as e:
            print(f"Failed to play movement sound: {str(e)}")