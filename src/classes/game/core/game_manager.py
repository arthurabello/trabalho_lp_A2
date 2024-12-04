"""
Core game manager handling initialization and main game loop.
"""

import pygame
from ..rendering.renderer import GameRenderer
from ..rendering.ui_renderer import UIRenderer
from .combat_manager import CombatManager
from ..input.input_handler import InputHandler
from ..turn.turn_manager import TurnManager
from .state_manager import GameStateManager
from ...board import Board

class GameManager:
    def __init__(self, player1_general=None, player2_general=None, map_choice=1):
        """Initialize the game manager and all subsystems."""
        try:
            pygame.init()
            if pygame.get_error():
                raise RuntimeError("Failed to initialize Pygame in game_manager/init")
                
        except Exception as e:
            raise RuntimeError(f"Failed to initialize game in game_manager/init: {str(e)}")
        
        self.state_manager = GameStateManager(player1_general, player2_general)
        self.setup_display()
        self.setup_managers(player1_general, player2_general, map_choice)

    def setup_display(self):
        """Setup the game display and window properties."""
        display_info = pygame.display.Info()
        self.max_screen_width = display_info.current_w
        self.max_screen_height = display_info.current_h
        self.windowed_width = self.state_manager.n * 50 + 300  #+300 for status screen
        self.windowed_height = self.state_manager.m * 50
        self.is_fullscreen = False
        self.screen_width = self.windowed_width
        self.screen_height = self.windowed_height
        self.board_width = self.state_manager.n * 50
        self.board_height = self.state_manager.m * 50

        try:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
            if not self.screen:
                raise RuntimeError("Failed to create game window in game_manager/init")
                
            self.background = pygame.Surface(self.screen.get_size())
            if not self.background:
                raise RuntimeError("Failed to create background surface in game_manager/init")
            
        except Exception as e:
            pygame.quit()
            raise RuntimeError(f"Failed to initialize display in game_manager/init: {str(e)}")

        pygame.display.set_caption("Warbound")

    def setup_managers(self, player1_general, player2_general, map_choice):
        """Initialize all game subsystem managers."""
        self.board = Board(self.state_manager.m, self.state_manager.n, 
                        self.board_width, self.board_height, [], 
                        map_choice=map_choice)
        
        self.state_manager.board = self.board
        
        self.state_manager.setup_units()
        
        self.renderer = GameRenderer(self.screen, self.board)
        self.ui_renderer = UIRenderer(self.screen)
        self.combat_manager = CombatManager(self.state_manager)
        self.input_handler = InputHandler(self)
        self.turn_manager = TurnManager(self.state_manager)

    def run(self):
        """Main game loop."""
        try:
            while self.state_manager.running:
                self.input_handler.handle_events()
                self.update()
                self.renderer.render(self.state_manager, self.ui_renderer)

        except Exception as e:
            print(f"Game crashed: {str(e)}")
        finally:
            pygame.quit()

    def update(self):
        """Update game state."""
        try:        
            self.renderer.draw_board()
                    
        except Exception as e:
            raise RuntimeError(f"Failed to draw the board: {str(e)}")

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        self.is_fullscreen = not self.is_fullscreen
        
        if self.is_fullscreen:
            self.screen_width = self.max_screen_width
            self.screen_height = self.max_screen_height
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        else:
            self.screen_width = self.windowed_width
            self.screen_height = self.windowed_height
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        
        self.background = pygame.Surface(self.screen.get_size())
        
        if self.is_fullscreen:
            game_area_width = self.screen_width - 300  
            width_scale = game_area_width / (self.state_manager.n * 50)
            height_scale = self.screen_height / (self.state_manager.m * 50)
            scale = min(width_scale, height_scale)
            
            self.board_width = int(self.state_manager.n * 50 * scale)
            self.board_height = int(self.state_manager.m * 50 * scale)
        else:
            self.board_width = self.state_manager.n * 50
            self.board_height = self.state_manager.m * 50
        
        self.renderer.update_surfaces(self.board_width, self.board_height)