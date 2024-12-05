"""
Manages combat interactions between units.
"""

class CombatManager:
    def __init__(self, state_manager):
        """Initialize combat manager."""
        self.state_manager = state_manager

    def handle_combat(self, attacker, defender):
        
        """
        Handle combat between attacker and defender.

        Args:
            attacker (BaseUnit): The unit that is attacking.
            defender (BaseUnit): The unit that is defending.

        Returns:
            bool: True if combat is successful, False otherwise.
        """

        if not self._validate_combat(attacker, defender):
            return False

        attacker.attack(defender, self.state_manager.board)
        
        if defender.has_general and not defender.is_alive:
            self.state_manager.game_over = True
            self.state_manager.winner = self.state_manager.current_player
        elif attacker.has_general and not attacker.is_alive:
            self.state_manager.game_over = True
            self.state_manager.winner = 3 - self.state_manager.current_player
            
        return True

    def _validate_combat(self, attacker, defender):
        
        """
        Check if combat is valid.

        Args:
            attacker (BaseUnit): The unit that is attacking.
            defender (BaseUnit): The unit that is defending.

        Returns:
            bool: True if combat is valid, False otherwise.
        """

        if not attacker.is_alive or not defender.is_alive:
            return False
            
        if attacker.player == defender.player:
            return False
            
        if attacker.has_attacked:
            return False
            
        return True

    def check_game_over(self):
        
        """
        Check if the game is over.
        """

        for player_units in [self.state_manager.units1, self.state_manager.units2]:
            has_general = False
            for unit in player_units:
                if unit.is_alive and unit.has_general:
                    has_general = True
                    break
            if not has_general:
                self.state_manager.game_over = True
                self.state_manager.winner = 2 if player_units == self.state_manager.units1 else 1
                break
            