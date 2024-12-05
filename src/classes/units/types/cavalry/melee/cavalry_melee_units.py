"""
Melee Cavalry unit type implementations.
"""

from ....base.base_unit import BaseUnit
import pygame
import os
from ....constants.paths import Paths

class LightHorsemen(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard") -> None:

        """
        Initialize light cavalry unit attributes.

        Args:
            initial_position (tuple): Initial position of the unit as a tuple of (row, col).
            player (int): Player number (1 or 2).
            movement_range (int): Movement range of the unit.
            formation (str, optional): Formation type. Default is "Standard".
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=3,
            formation=formation
        )
        self.attack_range = 1
        self.attack_type = "melee"
        self.base_attack = 50
        self.base_defense = 10
        self.base_missile_defense = 25
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Spread": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.2 #against ranged
            },
            "V": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6
            }
        }

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self) -> None:

        """
        Load sounds for light cavalry.
        """

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'lighthorsemen_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'lighthorsemen_attack.wav'))

    def _update_stats(self) -> None:

        """
        Update stats for light cavalry.
        """

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

class HeavyCavalry(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard") -> None:

        """
        Initialize heavy cavalry unit attributes.

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
        self.attack_range = 1
        self.attack_type = "melee"
        self.base_attack = 65
        self.base_defense = 30
        self.base_missile_defense = 35
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Spread": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.2 #against ranged
            },
            "V": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6
            }
        }

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self) -> None:
        
        """
        Load sounds for heavy cavalry.
        """

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'heavycavalry_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'heavycavalry_attack.wav'))

    def _update_stats(self) -> None:
        
        """
        Update stats for heavy cavalry.
        """

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp