"""
Formation-related functionality for units.
"""

import os
import pygame
from ..constants.paths import Paths
from .unit_direction import Direction
from ..constants.colors import Colors

class UnitFormationMixin:
    def change_formation(self, formation_name):
        """Change unit formation."""
        if formation_name in self.formations:
            self.formation = formation_name
            modifiers = self.formations[formation_name]
            
            self.attack_points = int(self.base_attack * modifiers['attack_modifier'])
            self.defense_points = int(self.base_defense * modifiers['defense_modifier'])

            self._update_sprite()

    def _update_sprite(self):
        """Update unit sprite based on formation and direction."""
        unit_type = self.__class__.__name__.lower()
        direction_str = Direction.to_string(self.facing_direction).lower()
        formation_name = self.formation.lower().replace(" ", "_")
        
        sprite_path = self._get_sprite_path(unit_type, formation_name, direction_str)
        self._load_and_color_sprite(sprite_path)

    def _get_sprite_path(self, unit_type, formation_name, direction_str):
        """Get path for unit sprite."""
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.normpath(os.path.join(current_file_path, "..", "..", "..", "assets"))
        
        return os.path.join(
            assets_path,
            "sprites",
            "units",
            unit_type,
            f"{unit_type}_{formation_name}_{direction_str.lower()}.png"
        )

    def _load_and_color_sprite(self, sprite_path):
        """Load and color sprite based on player."""
        sprite = self._load_sprite(sprite_path)
        
        if sprite:
            self.sprite = sprite.convert_alpha()
            colored_sprite = self.sprite.copy()
            
            overlay = pygame.Surface(self.sprite.get_size()).convert_alpha()
            overlay.fill(Colors.PLAYER1_PRIMARY_HOVER if self.player == 1 
                        else Colors.PLAYER2_PRIMARY_HOVER)
            colored_sprite.blit(overlay, (0,0))
            
            self.sprite = colored_sprite

    def _get_formation_modifier(self, attacker):
        """Get defense modifier based on formation."""
        if self.attack_type == "melee":
            if self.formation == "Shield Wall":
                if attacker.attack_type == "ranged":
                    return 2.5
                return 1.5
            elif self.formation == "Phalanx":
                if attacker.attack_type == "melee":
                    if self._is_frontal_attack(attacker):
                        return 3.0
                    return 0.8
                return 1.15
        elif self.attack_type == "ranged" and self.formation == "Spread":
            if attacker.attack_type == "ranged":
                return 1.6
            return 0.8
        return 1.0

    def _get_terrain_modifier(self, terrain, attacker):
        """Get defense modifier based on terrain."""
        if terrain == "mountain":
            if attacker.attack_type == "melee":
                return 1.5
            return 1.2
        elif terrain == "forest":
            if attacker.attack_type == "ranged":
                return 1.7
            return 1.25
        return 1.0