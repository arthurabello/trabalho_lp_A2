"""
Rendering-related functionality for units.
"""

import pygame
import os
from ..constants.colors import Colors
from ..constants.unit_defaults import UnitDefaults
from .unit_direction import Direction
from ..constants.paths import Paths

class UnitRenderingMixin:
    def draw(self, screen, board) -> None:

        """
        Draw unit on the screen.

        Args:
            screen (pygame.Surface): Surface to draw the unit on
            board (Board): Board instance
        """

        if not self.is_alive:
            return

        try:
            width, height = screen.get_size()
            if width <= 0 or height <= 0:
                raise ValueError("Invalid screen dimensions")

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

            if hasattr(self, 'sprite') and self.sprite is not None:
                self._draw_sprite(screen, x, y, unit_width, unit_height)

            self._draw_general_flag(screen, x, y, unit_width, unit_height)

        except Exception as e:
            raise RuntimeError(f"Failed to draw unit: {str(e)}")

    def _draw_sprite(self, screen, x, y, width, height) -> None:

        """
        Draw unit sprite on the screen.

        Args:
            screen (pygame.Surface): Surface to draw the sprite on
            x (int): X-coordinate of the top-left corner of the sprite
            y (int): Y-coordinate of the top-left corner of the sprite
            width (int): Width of the sprite
            height (int): Height of the sprite
        """

        try:
            resized_sprite = pygame.transform.scale(self.sprite, (width, height))
            screen.blit(resized_sprite, (x, y))
        except Exception as e:
            print(f"Failed to draw sprite: {e}")
    
    def _load_sprite(self, sprite_path) -> pygame.Surface | None:

        """Load sprite from the given path.
        
        Args:
            sprite_path (str): The path to the sprite image file.
        """

        try:
            if os.path.exists(sprite_path):
                return pygame.image.load(sprite_path)
            print(f"Sprite not found at: {sprite_path}")
            return None
        except Exception as e:
            print(f"Failed to load sprite: {str(e)}")
            return None

    def _update_sprite(self) -> None:

        """Update unit sprite based on formation and direction.
        
        This method constructs the appropriate path for the sprite based on the unit's type, 
        current formation, and direction, then loads and colors the sprite accordingly.
        """

        try:
            unit_type = self.__class__.__name__.lower()
            direction_str = Direction.to_string(self.facing_direction).lower()
            formation_name = self.formation.lower().replace(" ", "_")
            
            sprite_path = os.path.join(
                Paths.SPRITES_DIR,
                'units',
                unit_type,
                f"{unit_type}_{formation_name}_{direction_str}.png"
            )
            
            sprite = self._load_sprite(sprite_path)
            if sprite:
                self.sprite = sprite.convert_alpha()
                if hasattr(self, 'colors'):
                    colored_sprite = self.sprite.copy()
                    overlay = pygame.Surface(self.sprite.get_size()).convert_alpha()
                    overlay.fill(self.colors['hover'])
                    colored_sprite.blit(overlay, (0,0))
                    self.sprite = colored_sprite
            else:
                print(f"Failed to load sprite for {unit_type} with formation {formation_name}")
                
        except Exception as e:
            print(f"Failed to update sprite: {str(e)}")

    def draw_health_bar(self, screen, unit_x, unit_y, unit_width, unit_height) -> None:

        """
        Draw unit health bar.
        
        Args:
            screen (pygame.Surface): Surface to draw the health bar on
            unit_x (int): X-coordinate of the top-left corner of the unit
            unit_y (int): Y-coordinate of the top-left corner of the unit
            unit_width (int): Width of the unit
            unit_height (int): Height of the unit
        """

        if not self.is_alive:
            return
            
        health_percentage = self.current_hp / self.max_hp
        
        bar_width = 5
        bar_height = unit_height * 0.8

        if self.player == 1:
            bar_x = unit_x - bar_width - 5
        else:
            bar_x = unit_x + unit_width + 5
        bar_y = unit_y + (unit_height - bar_height) / 2

        pygame.draw.rect(screen, (64, 64, 64), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        filled_height = bar_height * health_percentage
        filled_y = bar_y + (bar_height - filled_height)
        
        color = (0, 255, 0) if health_percentage > 0.7 else \
                (255, 255, 0) if health_percentage > 0.3 else \
                (255, 0, 0)
                
        pygame.draw.rect(screen, color, 
                        (bar_x, filled_y, bar_width, filled_height))

    def _draw_general_flag(self, screen, x, y, unit_width, unit_height) -> None:

        """
        Draw general's flag if unit has general.
        
        Args:
            screen (pygame.Surface): Surface to draw the flag on
            x (int): X-coordinate of the top-left corner of the unit
            y (int): Y-coordinate of the top-left corner of the unit
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
            (flag_x + pole_width, flag_y + flag_height * 0.6)
        ]
        pygame.draw.polygon(screen, flag_color, flag_points)