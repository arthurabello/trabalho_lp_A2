"""
Melee Cavalry unit type implementations.
"""

from ....base.base_unit import BaseUnit
import pygame
import os
from ....constants.paths import Paths

class LightHorsemen(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard"):
        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=3,
            formation=formation
        )
        self.attack_range = 1
        self.attack_type = "melee"
        self.base_attack = 40
        self.base_defense = 12
        self.base_missile_defense = 25
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Spread": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.8
            },
            "V": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6
            }
        }

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self):
        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'lighthorsemen_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'lighthorsemen_attack.wav'))

    def _update_stats(self):
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp

class HeavyCavalry(BaseUnit):
    def __init__(self, initial_position, player, formation="Standard"):
        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=2,
            formation=formation
        )
        self.attack_range = 1
        self.attack_type = "melee"
        self.base_attack = 70
        self.base_defense = 20
        self.base_missile_defense = 35
        
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0
            },
            "Spread": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.8
            },
            "V": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6
            }
        }

        self._load_sounds()
        self._update_stats()
        self._update_sprite()

    def _load_sounds(self):
        self.move_sound = pygame.mixer.Sound(os.path.join(Paths.MOVE_SOUND_DIR, 'heavycavalry_movement.wav'))
        self.attack_sound = pygame.mixer.Sound(os.path.join(Paths.ATTACK_SOUND_DIR, 'heavycavalry_attack.wav'))

    def _update_stats(self):
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp