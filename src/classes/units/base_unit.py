"""
This module contains the abstract base class for all units in the game.
"""

import pygame
import os
from math import ceil
import random
from enum import IntEnum
from abc import ABC, abstractmethod
from .constants import Colors, Paths, UnitDefaults



class Direction(IntEnum):
    
    """
    Constant directions for unit movement
    
    Attributes:
        NORTH (int): North direction
        EAST (int): East direction
        SOUTH (int): South direction
        WEST (int): West direction
    """

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @classmethod
    def to_string(cls, direction):
        return {
            cls.NORTH: "North",
            cls.EAST: "East", 
            cls.SOUTH: "South",
            cls.WEST: "West"
        }[direction]
    
    @classmethod
    def get_covered_directions(cls, direction):
        
        """
        Returns a set of directions that are covered by the given direction
        
        Args:
            direction (Direction): The direction to check
        
        Returns:
            set: A set of directions
        """

        return {
            cls.NORTH: {cls.NORTH, cls.NORTH_EAST, cls.NORTH_WEST},
            cls.EAST: {cls.EAST, cls.NORTH_EAST, cls.SOUTH_EAST},
            cls.SOUTH: {cls.SOUTH, cls.SOUTH_EAST, cls.SOUTH_WEST},
            cls.WEST: {cls.WEST, cls.NORTH_WEST, cls.SOUTH_WEST}
        }[direction]

class BaseUnit(ABC):

    """
    Abstract base class for all units in the game.
    
    Attributes:
        position (tuple): Current position (row, col) on the board
        attack_points (int): The attack strength of the piece
        defense_points (int): The defense strength of the piece, reducing incoming damage
        remaining_units (int): Current units of the piece, representing its remaining units in the game
        formation (str): Current formation of the unit
        player (int): Player number (1 or 2) who owns this unit
        movement_range (int): Number of squares the unit can move
        size (tuple): Size of the unit graphic (width, height)
        is_alive (bool): Whether the unit is still alive
        primary_color (tuple): Main color of the unit based on player
        secondary_color (tuple): Secondary color based on player
    """
    
    def __init__(self, initial_position, player, movement_range, formation="Standard"):

        """
        Initialize a new unit with basic attributes and systems.
        
        Args:
            initial_position (tuple): Starting position as (row, col)
            player (int): Player number (1 or 2)
            movement_range (int): Number of squares the unit can move
            formation (str): Current formation of the unit
            
        Raises:
            ValueError: If position format is invalid or player number is not 1 or 2
            RuntimeError: If system initialization fails (font, sound, etc.)
        """

        if not isinstance(initial_position, tuple) or len(initial_position) != 2:
            raise ValueError("Initial position must be a tuple of (row, col) in units/base_unit")
        
        if not isinstance(player, int) or player not in [1, 2]:
            raise ValueError("Player must be 1 or 2")
        
        if movement_range < 0:
            raise ValueError("Movement range cannot be negative in units/base_unit")

        self.position = initial_position
        self.is_alive = True
        
        self.terrain = None
        self.general_id = None
        self.has_attacked = False
        self.facing_direction = Direction.EAST if player == 1 else Direction.WEST
        self.has_changed_direction = False

        self.attack_points = 0
        self.defense_points = 0

        self.formation = formation
        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "deffense_modifier": 1.0, 
            }
        }

        self.player = player
        self.movement_range = movement_range
        self.size = (0, 0)
        self._init_colors()
        self.has_general = False 
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.base_attack = 0  
        self.base_defense = 0   
        self.base_missile_defense = 0  
        self.attack_type = None  #"melee" or "ranged", set by subclasses
        self._init_systems()
        
    
    def _draw_general_flag(self, screen, x, y, unit_width, unit_height):

        """
        Draws a flag on top of the unit if it contains the general.
        
        Args:
            screen (pygame.Surface): Game screen to draw on
            x (int): X coordinate of the unit
            y (int): Y coordinate of the unit
            unit_width (int): Width of the unit
            unit_height (int): Height of the unit
        """
        
        if not self.has_general:
            return
            
        flag_height = unit_height * 0.3
        flag_width = unit_width * 0.4
        pole_width = flag_width * 0.1  
        
        flag_x = x + (unit_width - flag_width) / 2
        flag_y = y - flag_height
        pygame.draw.rect(screen, Colors.BORDER, 
                        (flag_x, flag_y, pole_width, flag_height))
        
        flag_color = Colors.PLAYER1_PRIMARY if self.player == 1 else Colors.PLAYER2_PRIMARY
        flag_points = [
            (flag_x + pole_width, flag_y),  
            (flag_x + flag_width, flag_y + flag_height * 0.3),  
            (flag_x + pole_width, flag_y + flag_height * 0.6),  
        ]
        pygame.draw.polygon(screen, flag_color, flag_points)

    def change_direction(self, new_direction):
        
        """
        Change the direction of the unit.
        
        Args:
            new_direction (Direction): New direction to face
        """

        if not self.has_changed_direction:
            self.facing_direction = new_direction
            self.has_changed_direction = True
            self._update_sprite()  
            return True
        return False
        
    def reset_direction_change(self):
        
        """
        Reset the direction change flag.
        """

        self.has_changed_direction = False
        
    def _load_direction_sprite(self, base_sprite_path):
        
        """
        Load a sprite based on the current facing direction.
        
        Args:
            base_sprite_path (str): Path to the base sprite
        """

        direction_str = Direction.to_string(self.facing_direction).lower()
        sprite_path = base_sprite_path.replace('.png', f'_{direction_str}.png')
        return self._load_sprite(sprite_path)

    def _init_colors(self):

        """
        Initialize primary and secondary colors based on player number.
        """

        if self.player == 1:
            self.primary_color = Colors.PLAYER1_PRIMARY
            self.secondary_color = Colors.PLAYER1_SECONDARY
        else:
            self.primary_color = Colors.PLAYER2_PRIMARY
            self.secondary_color = Colors.PLAYER2_SECONDARY
    
    def _init_systems(self):

        """
        Initialize font and sound systems for the unit.
        """

        try:
            if not pygame.font.get_init():
                pygame.font.init()
            self.font = pygame.font.Font(None, UnitDefaults.FONT_SIZE)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize font system in units/base_unit: {str(e)}")

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
                
            self.move_sound = pygame.mixer.Sound(Paths.MOVE_SOUND)
            self.attack_sound = pygame.mixer.Sound(Paths.ATTACK_SOUND)
            self.move_sound.set_volume(UnitDefaults.MOVE_SOUND_VOLUME)
            self.attack_sound.set_volume(UnitDefaults.ATTACK_SOUND_VOLUME)
            
        except Exception as e:
            print(f"Warning: Sound initialization failed in units/base_unit: {str(e)}")
            class DummySound:
                def play(self): pass
                def set_volume(self, vol): pass
            self.move_sound = DummySound()
            self.attack_sound = DummySound()

    def _load_sprite(self, sprite_path):

        """
        Load a sprite from a given path.

        Args:
            sprite_path (str): Path to the sprite image
        
        Returns:
            pygame.Surface: Loaded and converted sprite image
        """

        try:
            if os.path.exists(sprite_path):
                return pygame.image.load(sprite_path).convert_alpha()
            else:
                print(f"Warning: Sprite not found at {sprite_path}")
                return None
        except Exception as e:
            print(f"Error loading sprite {sprite_path}: {str(e)}")
            return None
    
    @abstractmethod
    def _update_sprite(self):
        
        """
        Update the sprite based on the current facing direction.
        """

        if self.formation in self.formation_sprites:
            base_sprite = self.formation_sprites[self.formation]
            sprite_path = os.path.dirname(base_sprite) + '/' + os.path.basename(base_sprite)
            self.sprite = self._load_direction_sprite(sprite_path)
        else:
            base_sprite = self.formation_sprites.get("Standard")
            sprite_path = os.path.dirname(base_sprite) + '/' + os.path.basename(base_sprite)
            self.sprite = self._load_direction_sprite(sprite_path)
            
        self.sprite = self.sprite.convert_alpha()
        colored_sprite = self.sprite.copy()
        
        if self.player == 1:
            overlay = pygame.Surface(self.sprite.get_size()).convert_alpha()
            overlay.fill((255, 0, 0, 40))
            colored_sprite.blit(overlay, (0,0))
        else:
            overlay = pygame.Surface(self.sprite.get_size()).convert_alpha()
            overlay.fill((0, 0, 255, 40))
            colored_sprite.blit(overlay, (0,0))
        
        self.sprite = colored_sprite
    
    def move(self, new_position):

        """
        Move the unit to a new position.
        
        Args:
            new_position (tuple): New position as (row, col)
        """

        if not self.is_alive:
            return

        self.position = new_position
        try:
            self.move_sound.play()
        except Exception as e:
            print(f"Failed to play movement sound in units/base_unit: {str(e)}")
    
    def _get_attack_direction(self, attacker):
        
        """
        Determines the direction of attack relative to the defender's facing direction.

        This function calculates whether an attack is coming from the front, flank, or rear 
        based on the relative positions of the attacker and defender, and the defender's 
        facing direction.

        How it works:
        1. First calculates relative positions:
        - rel_row = defender_row - attacker_row
        - rel_col = defender_col - attacker_col
        
        2. For each facing direction (NORTH, SOUTH, EAST, WEST):
        NORTH facing defender (defender looking up):
        - If attacker is below (rel_row > 0) = rear attack
        - If attacker is above (rel_row < 0) = front attack
        - If on same row = flank attack
        
        SOUTH facing defender (defender looking down):
        - If attacker is above (rel_row < 0) = rear attack
        - If attacker is below (rel_row > 0) = front attack
        - If on same row = flank attack
        
        EAST facing defender (defender looking right):
        - If attacker is to left (rel_col < 0) = rear attack
        - If attacker is to right (rel_col > 0) = front attack
        - If on same column = flank attack
        
        WEST facing defender (defender looking left):
        - If attacker is to right (rel_col > 0) = rear attack
        - If attacker is to left (rel_col < 0) = front attack
        - If on same column = flank attack

        Args:
            attacker (BaseUnit): The unit performing the attack
        
        Returns:
            str: Attack direction, one of:
                - "front": Attack is coming from the direction unit is facing
                - "rear": Attack is coming from behind
                - "flank": Attack is coming from the sides
        
        Examples:
            If defender at (5,5) facing NORTH:
            - Attacker at (4,5): Returns "front" (attacker is above)
            - Attacker at (6,5): Returns "rear" (attacker is below)
            - Attacker at (5,4): Returns "flank" (attacker is on same row)
        """
        
        att_row, att_col = attacker.position
        def_row, def_col = self.position
        
        rel_row = def_row - att_row 
        rel_col = def_col - att_col  
        
        match self.facing_direction:
            case Direction.NORTH:
                if rel_row > 0:
                    return "rear"
                elif rel_row < 0:  
                    return "front"
                else:  
                    return "flank"
                    
            case Direction.SOUTH:
                if rel_row < 0: 
                    return "rear"
                elif rel_row > 0: 
                    return "front"
                else:
                    return "flank"
                    
            case Direction.EAST:
                if rel_col < 0:  
                    return "rear"
                elif rel_col > 0: 
                    return "front"
                else:
                    return "flank"
                    
            case Direction.WEST:
                if rel_col > 0: 
                    return "rear"
                elif rel_col < 0: 
                    return "front"
                else:
                    return "flank"

    def attack(self, target, board):
        
        """
        Attack a target unit.
        """

        if not self.is_alive or not target.is_alive or target.player == self.player:
            return

        attack_direction = target._get_attack_direction(self)

        direction_mod = {
            "front": 1.0,
            "flank": 1.5, #this is changeable
            "rear": 2.0
        }[attack_direction]

        crit_chance = {
            "front": 0.05,
            "flank": 0.10, #this is changeable
            "rear": 0.15
        }[attack_direction]

        attack_mod = self._calculate_attack_modifiers()
        defense_mod = target._calculate_defense_modifiers(self, board)
        
        base_damage = (self.base_attack * attack_mod * direction_mod) * (1 - (target.base_defense * defense_mod / 100))
        
        variation = random.uniform(0.8, 1.2)
        if random.random() < crit_chance:
            variation *= 1.5
            
        final_damage = base_damage * variation
            
        target.current_hp = max(0, target.current_hp - final_damage)

        if self.attack_type == "melee" and target.attack_type == "melee":
            counter_mod = {
                "front": 0.6,
                "flank": 0.4, #changeable (counter-damage)
                "rear": 0.2
            }[attack_direction]
            
            counter_base = (target.base_attack * counter_mod) * (1 - (self.base_defense/100))
            counter_variation = random.uniform(0.8, 1.2)  
            
            counter_damage = counter_base * counter_variation
                
            self.current_hp = max(0, self.current_hp - counter_damage)
        
        if target.current_hp <= 0:
            target.is_alive = False
        if self.current_hp <= 0:
            self.is_alive = False
            
        self.has_attacked = True

    def can_attack(self, target_position):

        """
        Check if this unit can attack a position.
        
        Args:
            target_position (tuple): Position to check as (row, col)
            
        Returns:
            bool: True if the position is within attack range
        """

        if not self.is_alive:
            return False
            
        row, col = self.position
        target_row, target_col = target_position
        return abs(row - target_row) <= self.movement_range and abs(col - target_col) <= self.movement_range
    
    def change_formation(self, formation_name):

        """
        Change the formation of the unit.
        
        Args:
            formation_name (str): Name of the new formation
        """
        
        if formation_name in self.formations:
            self.formation = formation_name
            modifiers = self.formations[formation_name]
            
            self.attack_points = int(self.base_attack * modifiers['attack_modifier'])
            self.defense_points = int(self.base_defense * modifiers['defense_modifier'])

            self._update_sprite()



    def draw_health_bar(self, screen, unit_x, unit_y, unit_width, unit_height):
        
        """
        Draw the health bar for the unit.
        
        Args:
            screen (pygame.Surface): The surface to draw on
            unit_x (int): X position of the unit
            unit_y (int): Y position of the unit
            unit_width (int): Width of the unit
            unit_height (int): Height of the unit
        """

        if not self.is_alive:
            return
            
        health_percentage = self.current_hp / self.max_hp
        
        bar_width = 5 #changeable
        bar_height = unit_height * 0.8

        if self.player == 1:
            bar_x = unit_x - bar_width - 5  #left
        else:
            bar_x = unit_x + unit_width + 5  #right
        bar_y = unit_y + (unit_height - bar_height) / 2

        pygame.draw.rect(screen, (64, 64, 64), (bar_x, bar_y, bar_width, bar_height))
        
        filled_height = bar_height * health_percentage
        filled_y = bar_y + (bar_height - filled_height)
        
        color = (0, 255, 0) if health_percentage > 0.7 else \
                (255, 255, 0) if health_percentage > 0.3 else \
                (255, 0, 0)
                
        pygame.draw.rect(screen, color, (bar_x, filled_y, bar_width, filled_height))

    def draw(self, screen, board):

        """
        Draw the unit on the screen

        Args:
            screen (pygame.Surface): Game screen to draw on
            board (Board): The game board
        """

        if not self.is_alive:
            return

        try:
            width, height = screen.get_size()
            
            if width <= 0 or height <= 0:
                raise ValueError("Invalid screen dimensions in units/base_unit")

            square_width = width // board.n
            square_height = height // board.m
            
            self.size = (square_width, square_height)

            margin = square_width * (1 - UnitDefaults.UNIT_SCALE) / 2
            unit_width = square_width * UnitDefaults.UNIT_SCALE
            unit_height = square_height * UnitDefaults.UNIT_SCALE
            
            x = self.position[1] * square_width + margin
            y = self.position[0] * square_height + margin

            if board.selected_square == self.position:
                self.draw_health_bar(screen, x, y, unit_width, unit_height)

            pygame.draw.rect(screen, self.primary_color, (x, y, unit_width, unit_height))
            pygame.draw.rect(screen, Colors.BORDER, (x, y, unit_width, unit_height), 2)

            if hasattr(self, 'sprite') and self.sprite is not None:
                try:
                    resized_sprite = pygame.transform.scale(self.sprite, (unit_width, unit_height))
                    screen.blit(resized_sprite, (x, y))
                except Exception as e:
                    print(f"Failed to draw sprite: {e}") 


            self._draw_general_flag(screen, x, y, unit_width, unit_height)

        except Exception as e:
            print(f"Error in draw method: {str(e)}") 
            raise RuntimeError(f"Failed to draw unit in units/base_unit: {str(e)}")

    @abstractmethod
    def can_move_to(self, position, board, *args, **kwargs):

        """
        Abstract method that must be implemented by derived classes.
        Determines if the unit can move to a given position.
        
        Args:
            position (tuple): Target position to check
            board (Board): Game board instance
            *args, **kwargs: Additional arguments specific to unit types
            
        Returns:
            bool: True if the move is valid, False otherwise
        """
        pass
        
    @property
    def remaining_units(self):
        
        """
        Returns the number of units of the same type that are still alive.
        """

        return ceil(256 * (self.current_hp / self.max_hp))

    def _calculate_defense_modifiers(self, attacker, board):
        
        """
        Calculate total defense modifiers based on formation and general

        Args:
            attacker (BaseUnit): The attacking unit
            board (Board): The game board
        """

        modifiers = 1.0
        
        if self.has_general:
            modifiers *= 1.6 #alá o omi (motivação = 200%)

        if self.__class__.__name__ == "Hoplite": 
            if self.player == any(unit.player for unit in board.units if unit.has_general and unit.general_id == 'leonidas'):
                modifiers *= 1.1  
                
                if self.has_general and self.general_id == 'leonidas':
                    modifiers *= 1.15 
                
        row, col = self.position
        terrain = board.terrain.get((row, col))
        
        if terrain == "mountain":
            if attacker.attack_type == "melee":
                modifiers *= 1.5
            else:
                modifiers *= 1.2
        elif terrain == "forest":
            if attacker.attack_type == "ranged":
                modifiers *= 1.7
            else:
                modifiers *= 1.25
                
        if self.attack_type == "melee":
            if self.formation == "Shield Wall":
                if attacker.attack_type == "ranged":
                    modifiers *= 2.5
                else:
                    modifiers *= 1.5
            elif self.formation == "Phalanx":
                if attacker.attack_type == "melee":
                    if self._is_frontal_attack(attacker):
                        modifiers *= 3.0
                    else:
                        modifiers *= 0.8
                else:
                    modifiers *= 1.15
        elif self.attack_type == "ranged" and self.formation == "Spread": 
            if attacker.attack_type == "ranged":
                modifiers *= 1.6
            else:
                modifiers *= 0.8
                
        return modifiers

    def _calculate_attack_modifiers(self):
        
        """
        Calculate total attack modifiers based on formation and general
        """

        modifiers = 1.0
        
        if self.has_general:
            modifiers *= 1.25
            
        if self.attack_type == "melee" and self.formation == "Phalanx":
            modifiers *= 1.75
            
        return modifiers

    def _is_frontal_attack(self, attacker):
        
        """
        Determine if the attack is frontal

        Args:
            attacker (BaseUnit): The attacking unit
        """

        att_row, att_col = attacker.position
        def_row, def_col = self.position
        
        return abs(att_row - def_row) <= abs(att_col - def_col)

