"""
This module represents the main game structure, responsible for initializing, handling events, updating, and rendering the game.
"""

import pygame
from .board import Board
from .characters import King, Warrior

class Game:
    def __init__(self):
        
        try:
            pygame.init()
            if pygame.get_error():
                raise RuntimeError("Failed to initialize Pygame in game/init")
                
        except Exception as e:
            raise RuntimeError(f"Failed to initialize game in game/init: {str(e)}")
        
        self.m = 10
        self.n = 21
        if self.m <= 0 or self.n <= 0:
            raise ValueError("Invalid board dimensions in game/init")
        
        self.initial_width = self.n * 40
        self.initial_height = self.m * 40

        try:
            self.screen = pygame.display.set_mode((self.initial_width, self.initial_height), 
                                                pygame.RESIZABLE)
            if not self.screen:
                raise RuntimeError("Failed to create game window in game/init")
                
            self.background = pygame.Surface(self.screen.get_size())
            if not self.background:
                raise RuntimeError("Failed to create background surface in game/init")
            
        except Exception as e:
            pygame.quit()
            raise RuntimeError(f"Failed to initialize display in game/init: {str(e)}")

        self.screen = pygame.display.set_mode((self.initial_width, self.initial_height), 
                                            pygame.RESIZABLE)
        self.background = pygame.Surface(self.screen.get_size())
        
        pygame.display.set_caption("The Art of Violence")
        self.board = Board(self.m, self.n, self.initial_width, self.initial_height)
        self.running = True
        self.fullscreen = False
        self.current_size = [self.initial_width, self.initial_height]
        self.resizing = False
        
        self.king1 = King((0, self.n // 4), player=1)
        self.king2 = King((0, 3 * self.n // 4), player=2)
        
        self.warriors1 = self._create_warriors(1)
        self.warriors2 = self._create_warriors(2)
        
        self.selected_unit = None
        self.current_player = 1
        
        self.movement_points = {}  #tracks movement points for each unit
        self._reset_movement_points()
        
        self.game_over = False
        self.winner = None
        
        if not pygame.font.get_init():
            pygame.font.init()

        self.font = pygame.font.Font(None, 74)  #victory message
        self.small_font = pygame.font.Font(None, 36)  #UI elements
        self._draw_board()
    
    def _reset_movement_points(self):

        """
        Resets a player's movement points
        """
        
        all_units = self._get_player_units(self.current_player)
        for unit in all_units:
            self.movement_points[unit] = unit.movement_range

    def _get_player_units(self, player):

        """
        Get all of a player's units
        """

        if player == 1:
            return [self.king1] + self.warriors1
        else:
            return [self.king2] + self.warriors2

    def _create_warriors(self, player):

        """
        Position the warriors in a rectangular shape
        """

        warriors = []
        if player == 1:
            start_col = 2
        else:
            start_col = self.n - 7
            
        for row in range(2):
            for col in range(5):
                position = (row + 1, start_col + col)
                warrior = Warrior(position, player)
                warriors.append(warrior)
                
        return warriors
    
    def _get_all_units(self):

        """
        Returns a list of all units in the game
        """

        return ([self.king1, self.king2] + 
                self.warriors1 + 
                self.warriors2)
    
    def _get_unit_at_position(self, position):

        """
        Retrieves the unit at a given position if it exists and is alive

        Args:
            position (tuple): The (row, col) position to check

        Returns:
            Unit object if a unit is found at the specified position; otherwise, None
        """

        for unit in self._get_all_units():
            if unit.is_alive and unit.position == position:
                return unit
        return None
    
    def _draw_board(self):

        """
        Fills the background and draws the game board onto it
        """

        self.background.fill((0, 0, 0))
        self.board.draw(self.background, self.board.selected_square)

    def _draw_movement_points(self):

        """
        Draws the amount of movement points for a given unit as part of the UI
        """

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        padding = 10
        line_height = 30
        
        turn_text = f"Player {self.current_player}'s Turn - Press SPACE to end turn"
        mp_text = f"Movement Points: {self.movement_points.get(self.selected_unit, 0)}"
        
        turn_surface = self.small_font.render(turn_text, True, (255, 255, 255))
        mp_surface = self.small_font.render(mp_text, True, (255, 255, 255))
        
        ui_width = max(turn_surface.get_width(), mp_surface.get_width()) + (padding * 3)
        ui_height = (line_height * 2) + (padding * 2) 
        
        ui_surface = pygame.Surface((ui_width, ui_height))
        ui_surface.fill((0, 0, 0))
        ui_surface.set_alpha(128)
        
        ui_pos = (padding, screen_height - ui_height - padding)
        self.screen.blit(ui_surface, ui_pos) #bottom left corner
        
        self.screen.blit(turn_surface, (padding * 2, screen_height - line_height - padding))
        
        if self.selected_unit:
            self.screen.blit(mp_surface, (padding * 2, screen_height - (line_height * 2) - padding))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif not self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    clicked_square = self.board.get_square_from_click(mouse_position, self.screen)
                    
                    if clicked_square is None:
                        continue

                    if event.button == 1:  
                        clicked_unit = self._get_unit_at_position(clicked_square)
                        
                        if clicked_unit and clicked_unit.player == self.current_player:
                            self.selected_unit = clicked_unit
                            self.board.select_square(clicked_square, self.movement_points[clicked_unit])
                            self._draw_board()
                            
                        elif self.selected_unit and clicked_square in self.board.reachable_positions:
                            row1, col1 = self.selected_unit.position
                            row2, col2 = clicked_square
                            movement_cost = max(abs(row1 - row2), abs(col1 - col2))
                            
                            if self.movement_points[self.selected_unit] >= movement_cost:
                                target_unit = self._get_unit_at_position(clicked_square)
                                
                                if target_unit and target_unit.player != self.current_player:
                                    self.selected_unit.attack(target_unit)

                                    if isinstance(target_unit, King):
                                        self.game_over = True
                                        self.winner = self.current_player

                                    self.selected_unit.move(clicked_square)
                                    self.movement_points[self.selected_unit] -= movement_cost

                                elif not target_unit:
                                    self.selected_unit.move(clicked_square)
                                    self.movement_points[self.selected_unit] -= movement_cost
                                
                                if self.movement_points[self.selected_unit] <= 0:
                                    self.board.select_square(None, 0)
                                    self.selected_unit = None

                                else:
                                    self.board.select_square(clicked_square, 
                                                          self.movement_points[self.selected_unit])
                                self._draw_board()
                    
                    elif event.button == 3:  
                        self.selected_unit = None
                        self.board.select_square(None, 0)
                        self._draw_board()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.toggle_fullscreen()

                    elif event.key == pygame.K_SPACE:  
                        self.current_player = 3 - self.current_player
                        self.selected_unit = None
                        self.board.select_square(None, 0)
                        self._reset_movement_points()
                        self._draw_board()

            elif event.type == pygame.VIDEORESIZE:
                self.resizing = True
                self.current_size = [event.w, event.h]
    
    def toggle_fullscreen(self):

        """
        Toggles between fullscreen and windowed mode while maintaining aspect ratio.
        Handles screen scaling to prevent distortion.
        """

        try:
            screen_info = pygame.display.Info()
            
            if self.fullscreen:
                self.screen = pygame.display.set_mode(self.current_size, pygame.RESIZABLE)
            else:
                monitor_width = screen_info.current_w
                monitor_height = screen_info.current_h
                
                game_aspect_ratio = self.n / self.m  
                monitor_aspect_ratio = monitor_width / monitor_height
                
                if monitor_aspect_ratio > game_aspect_ratio:
                    new_height = monitor_height
                    new_width = int(new_height * game_aspect_ratio)
                else:
                    new_width = monitor_width
                    new_height = int(new_width / game_aspect_ratio)
                
                self.screen = pygame.display.set_mode((monitor_width, monitor_height), pygame.FULLSCREEN)
                
                self.scaled_size = (new_width, new_height)
                self.screen_offset = (
                    (monitor_width - new_width) // 2,
                    (monitor_height - new_height) // 2
                )
                
            self.fullscreen = not self.fullscreen
            if not self.fullscreen:
                self.current_size = list(self.screen.get_size())
            
            self.background = pygame.Surface(self.screen.get_size())
            self._draw_board()
            
        except Exception as e:
            print(f"Failed to toggle fullscreen: {str(e)}")
            self.fullscreen = False
            self.screen = pygame.display.set_mode(self.current_size, pygame.RESIZABLE)
    
    def render(self):

        """
        Renders the game screen, handling both windowed and fullscreen modes.
        In fullscreen mode, maintains aspect ratio and centers the game board.
        """

        self.screen.fill((0, 0, 0))
        
        if self.fullscreen:
            temp_surface = pygame.Surface(self.scaled_size)
            temp_surface.fill((0, 0, 0))
            
            scale_x = self.scaled_size[0] / self.initial_width
            scale_y = self.scaled_size[1] / self.initial_height
            
            scaled_background = pygame.transform.scale(self.background, self.scaled_size)
            temp_surface.blit(scaled_background, (0, 0))
            
            scaled_board = Board(self.m, self.n, self.scaled_size[0], self.scaled_size[1])
            
            self.king1.draw(temp_surface, scaled_board)
            self.king2.draw(temp_surface, scaled_board)
            
            for warrior in self.warriors1 + self.warriors2:
                warrior.draw(temp_surface, scaled_board)
            
            self._draw_movement_points()
            
            if self.game_over:
                self._draw_victory_message()
            
            self.screen.blit(temp_surface, self.screen_offset)
            
        else:
            self.screen.blit(self.background, (0, 0))
            self.king1.draw(self.screen, self.board)
            self.king2.draw(self.screen, self.board)
            
            for warrior in self.warriors1 + self.warriors2:
                warrior.draw(self.screen, self.board)
            
            self._draw_movement_points()
            
            if self.game_over:
                self._draw_victory_message()
        
        pygame.display.flip()
    
    def run(self):

        """
        Main game loop that handles the game execution.
        """

        try:
            while self.running:
                self.handle_events()
                self.update()
                self.render()

        except Exception as e:
            print(f"Game crashed: {str(e)}")
        finally:
            pygame.quit()

    def update(self):

        """
        Updates the game state, primarily handling window resizing events.
        Should be called every frame in the game loop.
        """

        try:
            if self.resizing:
                self.screen = pygame.display.set_mode(self.current_size, pygame.RESIZABLE)
                if not self.screen:
                    raise RuntimeError("Failed to resize window")
                    
                self.background = pygame.Surface(self.screen.get_size())
                if not self.background:
                    raise RuntimeError("Failed to create new background surface")
                    
                self._draw_board()
                self.resizing = False
                    
        except Exception as e:
            self.screen = pygame.display.set_mode(self.current_size, pygame.RESIZABLE)
            raise RuntimeError(f"Failed to update display: {str(e)}")
        
    def _draw_victory_message(self):
        if not self.game_over or self.winner is None:
            return
            
        message = f"Player {self.winner} Won!"
        text_surface = self.font.render(message, True, (255, 215, 0))  
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        background_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 40))
        background_surface.fill((0, 0, 0))
        background_surface.set_alpha(128)  #adjustable transparency
        
        background_rect = background_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        self.screen.blit(background_surface, background_rect)
        self.screen.blit(text_surface, text_rect)