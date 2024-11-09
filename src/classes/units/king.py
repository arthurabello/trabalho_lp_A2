"""
King unit implementation. The King is a special unit that, if defeated, ends the game.
It has limited movement but is crucial to protect.
"""

from .base_unit import BaseUnit
from .constants import Colors

class King(BaseUnit):

    """
    Represents a King piece on the game board.
    
    The King is a special unit that determines game victory/defeat.
    It has limited movement (1 square in any direction) but is vital to protect.
    
    Attributes:
        Inherits all attributes from BaseUnit
        special_ability_used (bool): Tracks if the king has used its special ability
    """
    
    def __init__(self, initial_position, player, image_path=None):

        """
        Initialize a new King unit.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
            image_path (str): Optional path to the king sprite image
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=1,
            unit_char='K',
            image_path=image_path
        )
        self.attack_points = 10
        self.defense_points = 5
        self.remaining_units = 100

        self.special_ability_used = False
        
        self.primary_color = (Colors.PLAYER1_PRIMARY if player == 1 
                            else Colors.PLAYER2_PRIMARY)
    
    def can_move_to(self, position, board, *args, **kwargs):

        """
        Check if the king can move to a given position.
        
        Kings can move one square in any direction (including diagonally)
        as long as the position is reachable on the board.
        
        Args:
            position (tuple): Target position to check
            board (Board): Game board instance
            
        Returns:
            bool: True if the move is valid, False otherwise
        """

        if not self.is_alive:
            return False
        
        reachable = board.graph.get_reachable_positions(
            self.position, 
            self.movement_range
        )
        return position in reachable

