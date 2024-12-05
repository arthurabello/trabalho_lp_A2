"""
Core base unit class providing fundamental unit attributes and methods.
"""

import pygame
from ..constants.paths import Paths
from ..constants.unit_defaults import UnitDefaults
from ..constants.colors import Colors
from .unit_combat import UnitCombatMixin
from .unit_movement import UnitMovementMixin
from .unit_rendering import UnitRenderingMixin
from .unit_formation import UnitFormationMixin
from .unit_direction import DirectionMixin
from .unit_direction import Direction

class BaseUnit(UnitCombatMixin, UnitMovementMixin, UnitRenderingMixin, UnitFormationMixin, DirectionMixin):
    """Base class for all units in the game."""
    def __init__(self, initial_position, player, movement_range, formation="Standard"):
        """
        Initialize base unit attributes.

        Args:
            initial_position (tuple): Initial position of the unit as a tuple of (row, col).
            player (int): Player number (1 or 2).
            movement_range (int): Movement range of the unit.
            formation (str, optional): Formation type. Default is "Standard".
        """
        if not isinstance(initial_position, tuple) or len(initial_position) != 2:
            raise ValueError("Initial position must be a tuple of (row, col)")
        
        if not isinstance(player, int) or player not in [1, 2]:
            raise ValueError("Player must be 1 or 2")
        
        if movement_range < 0:
            raise ValueError("Movement range cannot be negative")

        self.position = initial_position
        self.is_alive = True
        
        self.terrain = None
        self.general_id = None
        self.has_attacked = False
        self.facing_direction = Direction.EAST if player == 1 else Direction.WEST
        self.has_changed_direction = False

        self.formation = formation
        self.player = player
        self.movement_range = movement_range
        self.size = (0, 0)
        self.has_general = False 
        
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.base_attack = 0  
        self.base_defense = 0   
        self.base_missile_defense = 0  
        self.attack_type = None
        self.attack_range = 0
        
        self._init_colors()
        self._init_systems()


    def _init_colors(self):
            """
            Initialize unit colors based on player.
            """
            if self.player == 1:
                self.colors = {
                    'primary': Colors.PLAYER1_PRIMARY,
                    'secondary': Colors.PLAYER1_SECONDARY,
                    'hover': Colors.PLAYER1_PRIMARY_HOVER
                }
            else:
                self.colors = {
                    'primary': Colors.PLAYER2_PRIMARY,
                    'secondary': Colors.PLAYER2_SECONDARY,
                    'hover': Colors.PLAYER2_PRIMARY_HOVER
                }

    def _init_systems(self):
        """
        Initialize unit systems.
        """
        try:
            if pygame.mixer.get_init():
                self.move_sound = None
                self.attack_sound = None
            
            self._update_sprite()
            
        except Exception as e:
            print(f"Failed to initialize unit systems: {str(e)}")