"""
Handles all game input and events.
"""

import pygame
from .command_handler import CommandHandler

class InputHandler:
    def __init__(self, game_manager):
        """Initialize input handler."""
        self.game_manager = game_manager
        self.command_handler = CommandHandler(game_manager)
        self.state_manager = game_manager.state_manager

    def handle_events(self):
        """Process all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state_manager.running = False
                
            elif event.type == pygame.VIDEORESIZE:
                if not self.game_manager.is_fullscreen:
                    self.game_manager.screen = pygame.display.set_mode(
                        (event.w, event.h), pygame.RESIZABLE)
                    self.game_manager.toggle_fullscreen()
                    
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)

    def _handle_keydown(self, event):
        """Handle keyboard input."""
        if event.key == pygame.K_F11:
            self.game_manager.toggle_fullscreen()
        elif event.key == pygame.K_r and self.state_manager.game_over:
            self.command_handler.restart_game()
        elif event.key == pygame.K_m and self.state_manager.game_over:
            self.state_manager.running = False
        else:
            self.command_handler.handle_key_command(event.key)

    def _handle_mouse_click(self, event):
        """Handle mouse input."""
        mouse_pos = pygame.mouse.get_pos()
        
        if self.game_manager.is_fullscreen:
            board_y_offset = (self.game_manager.screen_height - self.game_manager.board_height) // 2
            adjusted_y = mouse_pos[1] - board_y_offset
            mouse_pos = (mouse_pos[0], adjusted_y)

        clicked_square = self.game_manager.board.get_square_from_click(
            mouse_pos, self.game_manager.renderer.board_surface)
            
        if clicked_square is None:
            return

        if event.button == 1:
            self.command_handler.handle_left_click(clicked_square)
        elif event.button == 3:
            self.command_handler.handle_right_click()