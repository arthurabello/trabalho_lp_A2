"""
Melee Infantry unit type implementations.
"""

from ....base.base_unit import BaseUnit
import pygame
import os
from ....constants.paths import Paths
from ....base.unit_combat import UnitCombatMixin

class Hoplite(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard") -> None:

        """
        Initialize hoplite unit attributes.

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
        self.base_attack = 60
        self.base_defense = 20
        self.base_missile_defense = 13
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Shield Wall": {
                "attack_modifier": 0.7,
                "defense_modifier": 1.8
            },
            "Phalanx": {
                "attack_modifier": 1.2,
                "defense_modifier": 1.6
            },
            "Spread": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0 #ranged will get bonus
            }
        }

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self) -> None:

        """
        Load sounds for hoplite.
        """

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'hoplite_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'hoplite_attack.wav'))

    def _update_stats(self) -> None:

        """
        Update stats for hoplite.
        """

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

class Legionary(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard") -> None:

        """
        Initialize legionary unit attributes.

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
        self.base_attack = 50
        self.base_defense = 22
        self.base_missile_defense = 15
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Shield Wall": {
                "attack_modifier": 0.7,
                "defense_modifier": 1.8
            },
            "Turtle": {
                "attack_modifier": 0.5,
                "defense_modifier": 1.2 #ranged will get bonus
            },
            "Spread": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.0 #ranged will get bonus
            }
        }

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self) -> None:

        """
        Load sounds for legionary.
        """

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'legionary_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'legionary_attack.wav'))

    def _update_stats(self) -> None:

        """
        Update stats for legionary.
        """

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

class Viking(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard") -> None:

        """   
        Initialize viking unit attributes.

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
        self.base_defense = 15
        self.base_missile_defense = 15
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Shield Wall": {
                "attack_modifier": 0.7,
                "defense_modifier": 1.8
            },
            "Spread": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0 #ranged will get bonus
            },
            "Turtle": {
                "attack_modifier": 0.5,
                "defense_modifier": 1.2
            },
            "V": {
                "attack_modifier": 1.5, #berserkergang uga buga
                "defense_modifier": 0.9
            }
        }

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self) -> None:

        """
        Load sounds for viking.
        """

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'viking_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'viking_attack.wav'))

    def _update_stats(self) -> None:

        """
        Update stats for viking.
        """

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

class Hypaspist(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard") -> None:

        """
        Initialize hypaspist unit attributes.

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
        self.base_attack = 45
        self.base_defense = 25
        self.base_missile_defense = 15
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Phalanx": {
                "attack_modifier": 1.2,
                "defense_modifier": 1.6
            },
            "Spread": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.0 #ranged will get bonus
            }
        }

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self) -> None:

        """
        Load sounds for hypaspist.
        """

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'hypaspist_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'hypaspist_attack.wav'))

    def _update_stats(self) -> None:

        """
        Update stats for hypaspist.
        """

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

class MenAtArms(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard") -> None:

        """
        Initialize men at arms unit attributes.

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
        self.base_attack = 50
        self.base_defense = 35
        self.base_missile_defense = 25
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Shield Wall": {
                "attack_modifier": 0.7,
                "defense_modifier": 1.8
            },
            "V": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6
            },
            "Turtle": {
                "attack_modifier": 0.5,
                "defense_modifier": 1.2 #ranged will get bonus
            },
            "Spread": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.0 #ranged will get bonus
            }
        }

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self) -> None:

        """
        Load sounds for men at arms.
        """

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'menatarms_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'menatarms_attack.wav'))

    def _update_stats(self) -> None:

        """
        Update stats for men at arms.
        """
        
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp