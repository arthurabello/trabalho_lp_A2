"""
Movement-related functionality for units.
"""

class UnitMovementMixin:
    def move(self, new_position):
        """Move unit to new position."""
        if not self.is_alive:
            return

        self.position = new_position
        self._play_move_sound()

    def can_move_to(self, position, board, all_units):
        """Check if unit can move to position."""
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