"""
This module contains the implementation of the Viking unit in the game.
"""

import os
import pygame
from .base_unit import BaseUnit
from .base_unit import UnitDefaults
from .constants import Colors

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

        sprite_dir = os.path.join('..', 'assets', 'sprites')
        self.formation_sprites = {
            "Standard": self._load_sprite(os.path.join(sprite_dir, 'viking.png')),
            "Shield Wall": self._load_sprite(os.path.join(sprite_dir, 'viking_shield_wall.png')),
            "Spread": self._load_sprite(os.path.join(sprite_dir, 'viking_spread.png')),
            "Turtle": self._load_sprite(os.path.join(sprite_dir, 'viking_turtle.png')),
            "V": self._load_sprite(os.path.join(sprite_dir, 'viking_V.png'))
        }

        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.max_hp = 100
        self.current_hp = self.max_hp


        self.primary_color = (Colors.PLAYER1_SECONDARY if player == 1 
                            else Colors.PLAYER2_SECONDARY)
        
        self._update_sprite()

    def draw(self, screen, board):
        
        """
        Draw the unit on the screen
        """

        if not self.is_alive:
            return

        width, height = screen.get_size()
        square_width = width // board.n
        square_height = height // board.m
        
        margin = square_width * (1 - UnitDefaults.UNIT_SCALE) / 2
        unit_width = square_width * UnitDefaults.UNIT_SCALE
        unit_height = square_height * UnitDefaults.UNIT_SCALE
        
        x = self.position[1] * square_width + margin
        y = self.position[0] * square_height + margin

        if board.selected_square == self.position:
            self.draw_health_bar(screen, x, y, unit_width, unit_height)

        if self.sprite:
            resized_sprite = pygame.transform.scale(self.sprite, (unit_width, unit_height))
            screen.blit(resized_sprite, (x, y))

        self._draw_general_flag(screen, x, y, unit_width, unit_height)
    
    def _update_sprite(self):

        """
        Updates the sprite based on the current formation and player number
        """

        if self.formation in self.formation_sprites:
            self.sprite = self.formation_sprites[self.formation]
        else:
            self.sprite = self.formation_sprites.get("Standard")
        
        self.sprite = self.sprite.convert_alpha()
        colored_sprite = self.sprite.copy()

        if self.player == 1:
            overlay = pygame.Surface(self.sprite.get_size()).convert_alpha()
            overlay.fill((255, 0, 0, 40))  
            colored_sprite.blit(overlay, (0,0))
        else:
            colored_sprite = pygame.transform.flip(colored_sprite, True, False)
            overlay = pygame.Surface(self.sprite.get_size()).convert_alpha()
            overlay.fill((0, 0, 255, 40))
            colored_sprite.blit(overlay, (0,0))
        
        self.sprite = colored_sprite


    def can_move_to(self, position, board, all_units):

        """
        Check if the Viking can move to a given position.
        
        Args:
            position (tuple): Target position to check
            board (Board): Game board instance
            all_units (list): List of all units on the board
            
        Returns:
            bool: True if the move is valid, False otherwise
        """

        if not self.is_alive:
            return False

        reachable = board.graph.get_reachable_positions(
            self.position, 
            self.movement_range
        )
        if position not in reachable:
            return False

        for unit in all_units:
            if (unit != self and unit.is_alive and 
                unit.position == position):
                return False

        return True

    def attack(self, target, board=None):

        """
        Attack another unit from range.
        
        Args:
            target: The unit being attacked
        """

        super().attack(target, board)
        
        try:
            self.attack_sound.play()
        except Exception as e:
            print(f"Failed to play attack sound in units/archer: {str(e)}")

    def can_attack(self, target_position):

        """
        Check if this viking can attack a position.
        
        Args:
            target_position (tuple): Position to check as (row, col)
            
        Returns:
            bool: True if the position is within attack range
        """
        
        if not self.is_alive:
            return False
            
        row, col = self.position
        target_row, target_col = target_position
        
        distance = abs(row - target_row) + abs(col - target_col)
        return distance <= self.attack_range

    def move_and_attack(self, target_unit, move_to_position, board):

        """
        Execute move-and-attack action
        """
        
        if move_to_position:
            self.move(move_to_position)
        self.attack(target_unit, board)
