"""
Manages game turns and related actions.
"""

class TurnManager:
    def __init__(self, state_manager) -> None:

        """
        Initialize the turn manager.

        Args:
            state_manager (StateManager): The state manager.
        """

        self.state_manager = state_manager
        
    def end_turn(self) -> None:
        
        """
        End the current player's turn.
        """

        self.state_manager.current_player = 3 - self.state_manager.current_player
        self.state_manager.selected_unit = None
        self.state_manager.selected_square = None
        self.state_manager._reset_movement_points()
        for unit in self.state_manager._get_player_units(self.state_manager.current_player):
            unit.has_attacked = False
            unit.reset_direction_change()
            
    def can_unit_act(self, unit) -> bool:
        
        """
        Checks if a unit can act this turn.

        Args:
            unit (Unit): The unit to check.

        Returns:
            bool: True if the unit can act, False otherwise.
        """

        if not unit.is_alive:
            return False
            
        if unit.player != self.state_manager.current_player:
            return False
            
        if self.state_manager.movement_points[unit] <= 0:
            return False
            
        return True
        
    def has_valid_moves(self, unit) -> bool:
        
        """
        Checks if unit can still move this turn.

        Args:
            unit (Unit): The unit to check.

        Returns:
            bool: True if the unit can still move, False otherwise.
        """

        return self.state_manager.movement_points[unit] > 0
        
    def has_valid_attacks(self, unit) -> bool:

        """
        Checks if unit can still attack this turn.

        Args:
            unit (Unit): The unit to check.

        Returns:
            bool: True if the unit can still attack, False otherwise.
        """

        return not unit.has_attacked