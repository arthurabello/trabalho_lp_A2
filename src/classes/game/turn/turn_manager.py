"""
Manages game turns and related actions.
"""

class TurnManager:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        
    def end_turn(self):
        """Handles the transition between player turns."""
        self.state_manager.current_player = 3 - self.state_manager.current_player
        self.state_manager.selected_unit = None
        self.state_manager.selected_square = None
        self.state_manager._reset_movement_points()
        for unit in self.state_manager._get_player_units(self.state_manager.current_player):
            unit.has_attacked = False
            unit.reset_direction_change()
            
    def can_unit_act(self, unit):
        """Checks if a unit can perform actions this turn."""
        if not unit.is_alive:
            return False
            
        if unit.player != self.state_manager.current_player:
            return False
            
        if self.state_manager.movement_points[unit] <= 0:
            return False
            
        return True
        
    def has_valid_moves(self, unit):
        """Checks if unit has any valid moves remaining."""
        return self.state_manager.movement_points[unit] > 0
        
    def has_valid_attacks(self, unit):
        """Checks if unit can still attack this turn."""
        return not unit.has_attacked