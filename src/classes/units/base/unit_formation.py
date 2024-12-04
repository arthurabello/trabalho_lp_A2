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
        """
        Calculates the formation modifier based on the attacker's attack type and the unit's current formation.
        """
        if not self.formation in self.formations:
            return 1.0
            
        formation_mod = self.formations[self.formation]['defense_modifier']
        
        if attacker.attack_type == "ranged":
            if self.formation == "Spread":
                return formation_mod * 1.2 #extra vs ranged
            elif self.formation == "Turtle" or self.formation == "Phalanx":
                return formation_mod * 1.2  #extra vs ranged saporra
            return formation_mod
            
        else:     
            if self.formation == "Phalanx":
                if self._is_frontal_attack(attacker):
                    if attacker.__class__.__name__ in ["HeavyCavalry", "LightHorsemen"]:
                        return formation_mod * 3.5  #lapada do satafera vs cavalo
                    return formation_mod * 2.5  #tapotente
                return formation_mod * 0.5  #flank penalty
            
            elif self.formation == "Spread":
                return formation_mod * 0.6 #negative melee vs spread
            
            elif self.formation == "Turtle":
                return 1.1 #lil bonus vs melee
            return formation_mod 


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