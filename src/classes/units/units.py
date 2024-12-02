"""
This module contains the classes for all units in the game.
"""

import os
import pygame
from .base_unit import BaseUnit
from .constants import Paths

class Hoplite(BaseUnit):

    """
    Represents a Hoplite piece on the game board.
    
    Attributes:
        Inherits all attributes from BaseUnit
        attack_bonus (int): Additional attack strength for this warrior
    """
    
    def __init__(self, initial_position, player, formation="Standard"):

        """
        Initialize a new Hoplite unit.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range=1
        self.attack_type = "melee"
        self.base_attack = 60
        self.base_defense = 15
        self.base_missile_defense = 30
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Shield Wall": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.8
            },
            "Phalanx": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6
            },
            "Spread": {
                "attack_modifier": 1.2,
                "defense_modifier": 0.9
            }
        }

        sprite_dir = os.path.join(Paths.SPRITES_DIR, 'units', 'hoplite')
        self.formation_sprites = {
            "Standard": self._load_sprite(os.path.join(sprite_dir, 'hoplite.png')),
            "Shield Wall": self._load_sprite(os.path.join(sprite_dir, 'hoplite_shield_wall.png')),
            "Phalanx": self._load_sprite(os.path.join(sprite_dir, 'hoplite_phalanx.png')),
            "Spread": self._load_sprite(os.path.join(sprite_dir, 'hoplite_spread.png'))
        }

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'hoplite_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'hoplite_attack.wav'))

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp
        
        self._update_sprite()

class Archer(BaseUnit):
    
    """
    Represents an Archer piece on the game board.
    
    Archers are ranged combat units with the ability to attack from a distance.
    Their unique feature is being able to attack enemies up to 2 squares away.
    
    Attributes:
        Inherits all attributes from BaseUnit
        attack_range (int): Range of squares the archer can attack from
    """
    
    def __init__(self, initial_position, player, formation="Standard"):

        """
        Initialize a new Archer unit.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
            formation (str): Initial formation of the unit
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_type = "ranged"
        self.base_attack = 22 #sus?
        self.base_defense = 2 
        self.attack_range = 2
        self.base_missile_defense = 8
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0,
            },
            "Spread": {
                "attack_modifier": 1.3,
                "defense_modifier": 0.8,
            }
        }


        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'archer_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'archer_attack.wav'))
        
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.base_attack = 20
        self.base_defense = 5
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense

        self._update_sprite()


class LightHorsemen(BaseUnit):

    """
    Represents a Cavalry piece on the game board.
    
    Attributes:
        Inherits all attributes from BaseUnit
        attack_bonus (int): Additional attack strength for this warrior
    """
    
    def __init__(self, initial_position, player, formation="Standard"):

        """
        Initialize a new Light Horsemen unit.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range=1
        self.attack_type = "melee"
        self.base_attack = 60
        self.base_defense = 15
        self.base_missile_defense = 30
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0,
            },
            "Spread": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.8,
            },
            "V": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6,
            }
        }

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'lighthorsemen_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'lighthorsemen_attack.wav'))

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp
        
        self._update_sprite()
        
class HeavyCavalry(BaseUnit):

    """
    Represents a Heavy cavalry piece on the game board.
    
    Attributes:
        Inherits all attributes from BaseUnit
        attack_bonus (int): Additional attack strength for this warrior
    """
    
    def __init__(self, initial_position, player, formation="Standard"):

        """
        Initialize a new Heavy cavalry unit.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range=1
        self.attack_type = "melee"
        self.base_attack = 60
        self.base_defense = 15
        self.base_missile_defense = 30
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0,
            },
            "Spread": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.8,
            },
            "V": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6,
            }
        }

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'heavycavalry_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'heavycavalry_attack.wav'))

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp
        
        self._update_sprite()

class MenAtArms(BaseUnit):

    """
    Represents a Men-at-Arms piece on the game board.
    
    Attributes:
        Inherits all attributes from BaseUnit
        attack_bonus (int): Additional attack strength for this warrior
    """
    
    def __init__(self, initial_position, player, formation="Standard"):

        """
        Initialize a new Men-at-Arms unit.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range=1
        self.attack_type = "melee"
        self.base_attack = 60
        self.base_defense = 15
        self.base_missile_defense = 22 #sus
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0, #sus
                "defense_modifier": 1.0
            },
            "Shield Wall": {
                "attack_modifier": 0.9, #sus
                "defense_modifier": 1.8
            },
             "V": {
                "attack_modifier": 1.5, #sus
                "defense_modifier": 0.6
            },
            "Turtle": {
                "attack_modifier": 0.5, #sus
                "defense_modifier": 1.5
            },
            "Spread": {
                "attack_modifier": 0.9, #sus
                "defense_modifier": 1.2
            }
        }

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'menatarms_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'menatarms_attack.wav'))

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

        self._update_sprite()

class Legionary(BaseUnit):

    """
    Represents a Legionary piece on the game board.
    
    Attributes:
        Inherits all attributes from BaseUnit
        attack_bonus (int): Additional attack strength for this warrior
    """
    
    def __init__(self, initial_position, player, formation="Standard"):

        """
        Initialize a new Legionary unit.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range=1
        self.attack_type = "melee"
        self.base_attack = 60
        self.base_defense = 15
        self.base_missile_defense = 30
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Shield Wall": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.8
            },
            "Turtle": {
                "attack_modifier": 0.5,
                "defense_modifier": 1.3
            },
            "Spread": {
                "attack_modifier": 1.2,
                "defense_modifier": 0.9
            }
        }

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'legionary_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'legionary_attack.wav'))

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

        self._update_sprite()


class Hypaspist(BaseUnit):

    """
    Represents a Hypaspist piece on the game board.
    
    Attributes:
        Inherits all attributes from BaseUnit
        attack_bonus (int): Additional attack strength for this warrior
    """
    
    def __init__(self, initial_position, player, formation="Standard"):

        """
        Initialize a new Hypaspist unit.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range=1
        self.attack_type = "melee"
        self.base_attack = 60
        self.base_defense = 15
        self.base_missile_defense = 30
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Shield Wall": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.8
            },
            "Phalanx": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6
            },
            "Spread": {
                "attack_modifier": 1.2,
                "defense_modifier": 0.9
            }
        }

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'hypaspist_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'hypaspist_attack.wav'))
 
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

        self._update_sprite()

class Crossbowman(BaseUnit):
    
    """
    Represents an Crossbowman piece on the game board.
    
    Crossbowman are ranged combat units with the ability to attack from a distance.
    Their unique feature is being able to attack enemies up to 3 squares away.
    
    Attributes:
        Inherits all attributes from BaseUnit
        attack_range (int): Range of squares the crossbowman can attack from
    """
    
    def __init__(self, initial_position, player, formation="Standard"):

        """
        Initialize a new Crossbowman unit.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
            formation (str): Initial formation of the unit
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
                "defense_modifier": 1.0,
            },
            "Spread": {
                "attack_modifier": 1.3,
                "defense_modifier": 0.8,
            }
        }
        
        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'crossbowman_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'crossbowman_attack.wav'))

        self.max_hp = 100
        self.current_hp = self.max_hp
        self.base_attack = 20
        self.base_defense = 5
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense

        self._update_sprite()


class Viking(BaseUnit):

    """
    Represents a Viking piece on the game board.
    
    Attributes:
        Inherits all attributes from BaseUnit
        attack_bonus (int): Additional attack strength for this warrior
    """
    
    def __init__(self, initial_position, player, formation="Standard"):

        """
        Initialize a new Viking unit.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range=1
        self.attack_type = "melee"
        self.base_attack = 60
        self.base_defense = 15
        self.base_missile_defense = 30
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Shield Wall": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.8
            },
            "Spread": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6
            },
            "Turtle": {
                "attack_modifier": 0.4,
                "defense_modifier": 2.0
            },
            "V": {
                "attack_modifier": 1.3,
                "defense_modifier": 0.9
            }
        }

        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'viking_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'viking_attack.wav'))

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

        self._update_sprite()