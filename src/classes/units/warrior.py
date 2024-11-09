"""
Warrior unit implementation. Warriors are the main combat units with
greater mobility than Kings but less strategic importance.
"""

from .base_unit import BaseUnit
from .constants import Colors

class Warrior(BaseUnit):

    """
    Represents a Warrior piece on the game board.
    
    Warriors are the main combat units with extended movement range
    and the ability to attack enemies.
    
    Attributes:
        Inherits all attributes from BaseUnit
        attack_bonus (int): Additional attack strength for this warrior
    """
    
    def __init__(self, initial_position, player, image_path=None, formation="Standard"):

        """
        Initialize a new Warrior unit.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
            image_path (str): Optional path to the warrior sprite image
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=3,
            unit_char='W',
            image_path=image_path,
            formation=formation
        )

        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0,
            },
            "Defensive": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.8,
            },
            "Aggressive": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6,
            }
        }

        self.base_attack = 10
        self.base_defense = 5

        # current stats (will be modified by formations)
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense

        self.remaining_units = 256

        self.primary_color = (Colors.PLAYER1_SECONDARY if player == 1 
                            else Colors.PLAYER2_SECONDARY)
    
    def can_move_to(self, position, board, all_units):

        """
        Check if the warrior can move to a given position.
        
        Warriors can move up to three squares in any direction, but cannot
        move through or onto other units.
        
        Args:
            position (tuple): Target position to check
            board (Board): Game board instance
            all_units (list): List of all units on the board
            
        Returns:
            bool: True if the move is valid, False otherwise
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
    
    def attack(self, target):

        """
        Enhanced attack method for Warriors.
        Warriors get an attack bonus when attacking.
        
        Args:
            target: The unit being attacked
        """

        if not self.is_alive or not target.is_alive or target.player == self.player:
            return
            
        try:
            self.attack_sound.play()
        except Exception as e:
            print(f"Failed to play warrior attack sound in units/warrior: {str(e)}")
            
        target.is_alive = False