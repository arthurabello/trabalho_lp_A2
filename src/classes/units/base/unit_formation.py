"""
Formation-related functionality for units.
"""

import os
import pygame
from ..constants.paths import Paths
from .unit_direction import Direction
from ..constants.colors import Colors

class UnitFormationMixin:
    """
    Mixin class for handling unit formations and related functionality.
    
    This class provides methods for changing unit formations, updating sprites based on 
    formation and direction, and calculating formation-based modifiers.
    """
    def change_formation(self, formation_name):
        """
        Changes the unit's formation and updates the corresponding stats.
        
        This method updates the unit's attack and defense points based on the modifiers 
        associated with the new formation. It also updates the unit's sprite based on the 
        new formation and direction.
        
        Args:
            formation_name (str): The name of the new formation to switch to.

        """
        if formation_name in self.formations:
            self.formation = formation_name
            modifiers = self.formations[formation_name]
            
            self.attack_points = int(self.base_attack * modifiers['attack_modifier'])
            self.defense_points = int(self.base_defense * modifiers['defense_modifier'])

            self._update_sprite()

    def _update_sprite(self):
        """
        Updates the unit's sprite based on its formation and facing direction.
        
        This method constructs the appropriate path for the sprite based on the unit's type, 
        current formation, and direction, then loads and colors the sprite accordingly.
        """
        unit_type = self.__class__.__name__.lower()
        direction_str = Direction.to_string(self.facing_direction).lower()
        formation_name = self.formation.lower().replace(" ", "_")
        
        sprite_path = self._get_sprite_path(unit_type, formation_name, direction_str)
        self._load_and_color_sprite(sprite_path)

    def _get_sprite_path(self, unit_type, formation_name, direction_str):
        """
        Constructs the path to the unit's sprite based on its type, formation, and direction.
        
        Args:
            unit_type (str): The type of the unit (e.g., "infantry", "cavalry").
            formation_name (str): The name of the current formation (e.g., "spread", "phalanx").
            direction_str (str): The string representation of the direction (e.g., "north", "east").
        
        Returns:
            str: The file path to the unit's sprite image.
        """
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
        """
        Loads and colors the unit's sprite based on the player's faction.
        
        The sprite is loaded from the given path, and a color overlay is applied based on 
        the player's faction (Player 1 or Player 2).
        
        Args:
            sprite_path (str): The file path to the unit's sprite image.
        """
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
        Calculates the defense modifier based on the unit's current formation and the attacker's attack type.
        
        The modifier is influenced by both the unit's formation and the attacker's attack type (melee or ranged).
        
        Args:
            attacker (BaseUnit): The unit attacking this unit, used to determine the attack type.
        
        Returns:
            float: The defense modifier based on the formation and the attacker's attack type.
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
        """
        Returns the defense modifier based on the terrain type.
        
        The defense modifier varies depending on whether the terrain is a mountain, forest, or normal terrain.
        
        Args:
            terrain (str): The type of terrain (e.g., "mountain", "forest").
            attacker (BaseUnit): The attacking unit, used to determine the attack type.
        
        Returns:
            float: The defense modifier based on the terrain type and attacker's attack type.
        """
        if terrain == "mountain":
            if attacker.attack_type == "melee":
                return 1.5
            return 1.2
        elif terrain == "forest":
            if attacker.attack_type == "ranged":
                return 1.7
            return 1.25
        return 1.0