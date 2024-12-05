"""
Main renderer responsible for game visualization.
"""

import pygame

class GameRenderer:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.base_surface = pygame.Surface((board.initial_width, board.initial_height))
        self.board_surface = self.base_surface.copy()
        self.background = pygame.Surface(screen.get_size())
        self.init_fonts()

    def update_surfaces(self, board_width, board_height):
        """Update dimensions while maintaining base surface"""
        self.board_width = board_width
        self.board_height = board_height
        self.board_surface = self.base_surface.copy()
        self.background = pygame.Surface(self.screen.get_size())

    def render(self, state_manager, ui_renderer):
        self.screen.fill((0, 0, 0))
        self.board_surface.fill((0, 0, 0))
        
        self.board.draw(self.board_surface, state_manager.selected_square)
        for unit in state_manager.get_all_units():
            if unit.is_alive:
                unit.draw(self.board_surface, self.board)

        if self.board.is_fullscreen:
            game_width = self.screen.get_width() - 300  
            game_height = self.screen.get_height()
            
            width_scale = game_width / self.board.initial_width
            height_scale = game_height / self.board.initial_height
            scale = min(width_scale, height_scale)
            
            actual_width = int(self.board.initial_width * scale)
            actual_height = int(self.board.initial_height * scale)
            
            scaled = pygame.transform.smoothscale(self.board_surface, (actual_width, actual_height))
            
            board_y = (game_height - actual_height) // 2
            
            self.board.board_width = actual_width
            self.board.board_height = actual_height
            
            self.screen.blit(scaled, (0, board_y))
        else:
            self.screen.blit(self.board_surface, (0, 0))
            self.board.board_width = self.board.initial_width
            self.board.board_height = self.board.initial_height

        ui_renderer.render(state_manager)
        
        if state_manager.game_over:
            self._draw_victory_message(state_manager.winner)
        
        pygame.display.flip()

    def init_fonts(self):
        """Initialize fonts for rendering."""
        if not pygame.font.get_init():
            pygame.font.init()
        self.victory_font = pygame.font.Font(None, 74)
        self.normal_font = pygame.font.Font(None, 36)
        
        
    def draw_board(self):
        """Refresh the board drawing."""
        self.background.fill((0, 0, 0))
        self.board.draw(self.board_surface, self.board.selected_square)
        
    def _draw_victory_message(self, winner):
        """Draw the victory screen."""
        if not winner:
            return
            
        message = f"Player {winner} Won!"
        text_surface = self.victory_font.render(message, True, (255, 215, 0))
        
        instructions = "Press R to restart or M to return to menu"
        instructions_surface = self.normal_font.render(instructions, True, (255, 255, 255))
        
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 20))
        instructions_rect = instructions_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 40))
        
        total_height = text_rect.height + instructions_rect.height + 60
        max_width = max(text_rect.width, instructions_rect.width) + 40

        background_surface = pygame.Surface((max_width, total_height))
        background_surface.fill((0, 0, 0))
        background_surface.set_alpha(128)
        
        background_rect = background_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        self.screen.blit(background_surface, background_rect)
        self.screen.blit(text_surface, text_rect)
        self.screen.blit(instructions_surface, instructions_rect)