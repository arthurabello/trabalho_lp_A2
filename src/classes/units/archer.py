"""
This module contains the implementation of the Archer unit in the game.
"""

from .base_unit import BaseUnit
from .base_unit import UnitDefaults
from .constants import Colors
import os
import pygame

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

        sprite_dir = os.path.join('..', 'assets', 'sprites', 'units', 'archer')
        self.formation_sprites = {
            "Standard": self._load_sprite(os.path.join(sprite_dir, 'archer.png')),
            "Spread": self._load_sprite(os.path.join(sprite_dir, 'archer_spread.png'))
        }
        
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.base_attack = 20
        self.base_defense = 5
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense
        self.primary_color = (Colors.PLAYER1_SECONDARY if player == 1 else Colors.PLAYER2_SECONDARY)
        self._update_sprite()
    
    def draw(self, screen, board):
        
        """
        Draw the unit and handle arrow animation
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
        Check if this archer can attack a position.
        
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
        
        return distance <= self.attack_range and distance > 0

    def _update_sprite(self):

        """
        Updates the sprite based on the current formation.
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
        Check if the archer can move to a given position.
        
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