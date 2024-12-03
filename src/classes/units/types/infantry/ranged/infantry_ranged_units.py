"""
Ranged Infantry unit type implementations.
"""

from ....base.base_unit import BaseUnit
import pygame
import os
from ....constants.paths import Paths

class Archer(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard"):
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

    def _load_sounds(self):
        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'archer_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'archer_attack.wav'))

    def _update_stats(self):
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense

class Crossbowmen(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard"):
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

    def _load_sounds(self):
        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'crossbowman_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'crossbowman_attack.wav'))

    def _update_stats(self):
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense