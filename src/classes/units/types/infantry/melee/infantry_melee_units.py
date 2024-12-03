"""
Melee Infantry unit type implementations.
"""

from ....base.base_unit import BaseUnit
import pygame
import os
from ....constants.paths import Paths
from ....base.unit_combat import UnitCombatMixin

class Hoplite(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard"):
        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range = 1
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

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self):
        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'hoplite_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'hoplite_attack.wav'))

    def _update_stats(self):
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

class Legionary(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard"):
        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range = 1
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

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self):
        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'legionary_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'legionary_attack.wav'))

    def _update_stats(self):
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

class Viking(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard"):
        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range = 1
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

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self):
        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'viking_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'viking_attack.wav'))

    def _update_stats(self):
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

class Hypaspist(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard"):
        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range = 1
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

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self):
        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'hypaspist_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'hypaspist_attack.wav'))

    def _update_stats(self):
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

class MenAtArms(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard"):
        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range = 1
        self.attack_type = "melee"
        self.base_attack = 60
        self.base_defense = 15
        self.base_missile_defense = 22
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Shield Wall": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.8
            },
            "V": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6
            },
            "Turtle": {
                "attack_modifier": 0.5,
                "defense_modifier": 1.5
            },
            "Spread": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.2
            }
        }

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self):
        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'menatarms_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'menatarms_attack.wav'))

    def _update_stats(self):
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp