"""
This module contains the abstract base class for all units in the game.
"""

import pygame
import os
import random
from abc import ABC, abstractmethod
from .constants import Colors, Paths, UnitDefaults

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
            formatior (str): Current formation of the unit
            
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
        self.attack_points = 0
        self.defense_points = 0
        self.remaining_units = 0
        self.formation = formation
        self.formations = {
            "normal": {
                "attack_modifier": 1.0,
                "deffense_modifier": 1.0, 
            }
        }
        self.action = "Move"
        self.actions = ["Move", "Attack"]

        self.player = player
        self.movement_range = movement_range
        self.size = (0, 0)
        self.is_alive = True
        self._init_colors()
        self.has_general = False 
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
        Update the current sprite based on formation.
        Should be implemented by derived classes.
        """

        pass
    
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

    def attack(self, target):

        """
        Attack another unit.
        
        Args:
            target: The unit being attacked
        """

        if not self.is_alive or not target.is_alive or target.player == self.player:
            return
            
        try:
            self.attack_sound.play()
        except Exception as e:
            print(f"Failed to play attack sound in units/base_unit: {str(e)}")

        chance_of_success = self.attack_points / (self.attack_points + target.defense_points)
            
        if random.random() < chance_of_success:
            target.is_alive = False
        else:
            self.is_alive = False

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
        Change the unit's formation and apply corresponding modifiers.
        
        Args:
            formation_name (str): Name of the formation to switch to
        """

        if formation_name in self.formations:
            self.formation = formation_name
            modifiers = self.formations[formation_name]
            
            self.attack_points = int(self.base_attack * modifiers['attack_modifier'])
            self.defense_points = int(self.base_defense * modifiers['defense_modifier'])

            self._update_sprite()


    def change_action(self, action_name):

        """
        Change the unit's action

        Args:
            action_name (str): Name of the formation to switch to
        """
        if action_name in self.actions:
            self.action = action_name


    def draw(self, screen, board):

        """
        Draw the unit on the screen.
        """

        if not self.is_alive:
            return

        try:
            width, height = screen.get_size()
            print(f"Screen dimensions: {width}x{height}") 
            
            if width <= 0 or height <= 0:
                raise ValueError("Invalid screen dimensions in units/base_unit")

            square_width = width // board.n
            square_height = height // board.m
            
            print(f"Square dimensions: {square_width}x{square_height}")  
            
            self.size = (square_width, square_height)

            margin = square_width * (1 - UnitDefaults.UNIT_SCALE) / 2
            unit_width = square_width * UnitDefaults.UNIT_SCALE
            unit_height = square_height * UnitDefaults.UNIT_SCALE
            
            x = self.position[1] * square_width + margin
            y = self.position[0] * square_height + margin
            
            print(f"Drawing unit at: {x},{y} with size {unit_width}x{unit_height}") 

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