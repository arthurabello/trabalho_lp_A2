"""
Warrior unit implementation. Warriors are the main combat units with
greater mobility than Kings but less strategic importance.
"""

import os
import pygame
from .base_unit import BaseUnit
from .base_unit import UnitDefaults
from .constants import Colors

class Warrior(BaseUnit):

    """
    Represents a Warrior piece on the game board.
    
    Warriors are the main combat units with extended movement range
    and the ability to attack enemies.
    
    Attributes:
        Inherits all attributes from BaseUnit
        attack_bonus (int): Additional attack strength for this warrior
    """
    
    def __init__(self, initial_position, player, formation="Standard"):

        """
        Initialize a new Warrior unit.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
        """

        super().__init__(
            initial_position=initial_position,
            player=player,
            movement_range=3,
            unit_char='W',
            formation=formation
        )

        self.formations = {
            "Standard": {
                "attack_modifier": 1.0,
                "defense_modifier": 1.0,
            },
            "Defensive": {
                "attack_modifier": 0.9,
                "defense_modifier": 1.8,
            },
            "Aggressive": {
                "attack_modifier": 1.5,
                "defense_modifier": 0.6,
            }
        }

        sprite_dir = os.path.join('..', 'assets', 'sprites')
        self.formation_sprites = {
            "Standard": self._load_sprite(os.path.join(sprite_dir, 'warrior.png')),
            "Defensive": self._load_sprite(os.path.join(sprite_dir, 'warrior_defense.png')),
            "Aggressive": self._load_sprite(os.path.join(sprite_dir, 'warrior_attack.png'))
        }

        self.base_attack = 10
        self.base_defense = 5

        # current stats (will be modified by formations)
        self.attack_points = self.base_attack
        self.defense_points = self.base_defense

        self.remaining_units = 256

        self.primary_color = (Colors.PLAYER1_SECONDARY if player == 1 
                            else Colors.PLAYER2_SECONDARY)
        
        self._update_sprite()

    def draw(self, screen, board):
        """Override draw method to ensure visibility even without sprites"""
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

        if not hasattr(self, 'sprite') or self.sprite is None:
            pygame.draw.rect(screen, self.primary_color, (x, y, unit_width, unit_height))
            pygame.draw.rect(screen, Colors.BORDER, (x, y, unit_width, unit_height), 2)
            
            text_surface = self.font.render('W', True, Colors.TEXT)
            text_rect = text_surface.get_rect(center=(x + unit_width/2, y + unit_height/2))
            screen.blit(text_surface, text_rect)
        else:
            resized_sprite = pygame.transform.scale(self.sprite, (unit_width, unit_height))
            screen.blit(resized_sprite, (x, y))

        self._draw_general_flag(screen, x, y, unit_width, unit_height)
    
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
            overlay.fill((255, 0, 0, 60))  
            colored_sprite.blit(overlay, (0,0))
        else:
            overlay = pygame.Surface(self.sprite.get_size()).convert_alpha()
            overlay.fill((0, 0, 255, 60))
            colored_sprite.blit(overlay, (0,0))
        
        self.sprite = colored_sprite


    def can_move_to(self, position, board, all_units):

        """
        Check if the warrior can move to a given position.
        
        Warriors can move up to three squares in any direction, but cannot
        move through or onto other units.
        
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
    
    # def attack(self, target):

    #     """
    #     Enhanced attack method for Warriors.
    #     Warriors get an attack bonus when attacking.
        
    #     Args:
    #         target: The unit being attacked
    #     """

    #     if not self.is_alive or not target.is_alive or target.player == self.player:
    #         return
            
    #     try:
    #         self.attack_sound.play()
    #     except Exception as e:
    #         print(f"Failed to play warrior attack sound in units/warrior: {str(e)}")
            
    #     target.is_alive = False