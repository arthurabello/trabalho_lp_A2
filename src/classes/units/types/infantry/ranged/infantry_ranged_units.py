"""
Ranged Infantry unit type implementations.
"""

from ....base.base_unit import BaseUnit
import pygame
import os
from ....constants.paths import Paths

class Archer(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard") -> None:
        
        """
        Initialize archer unit attributes.

        Args:
            initial_position (tuple): Initial position of the unit as a tuple of (row, col).
            player (int): Player number (1 or 2).
            movement_range (int): Movement range of the unit.
            formation (str, optional): Formation type. Default is "Standard".
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_type = "ranged"
        self.base_attack = 22
        self.base_defense = 2 
        self.attack_range = 2
        self.base_missile_defense = 8
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Spread": {
                "attack_modifier": 1.3,
                "defense_modifier": 0.8
            }
        }

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self) -> None:

        """
        Load sounds for archer.
        """

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'archer_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'archer_attack.wav'))

    def _update_stats(self) -> None:

        """
        Update stats for archer.
        """

        self.max_hp = 100
        self.current_hp = self.max_hp
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense

class Crossbowmen(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard") -> None:

        """
        Initialize crossbowmen unit attributes.

        Args:
            initial_position (tuple): Initial position of the unit as a tuple of (row, col).
            player (int): Player number (1 or 2).
            movement_range (int): Movement range of the unit.
            formation (str, optional): Formation type. Default is "Standard".
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_type = "ranged"
        self.base_attack = 30
        self.base_defense = 2 
        self.attack_range = 3
        self.base_missile_defense = 8
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Spread": {
                "attack_modifier": 1.3,
                "defense_modifier": 0.8
            }
        }

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self) -> None:

        """
        Load sounds for crossbowmen.
        """

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'crossbowman_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'crossbowman_attack.wav'))

    def _update_stats(self) -> None:

        """
        Update stats for crossbowmen.
        """
        
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense