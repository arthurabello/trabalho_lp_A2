"""
This module represents the main game structure, responsible for initializing, handling events, updating, and rendering the game.
"""

import pygame
from .board import Board
from .units.hoplite import Hoplite
from .menu.menu import Menu
from .units.archer import Archer

class Game:
    def __init__(self):
        try:
            pygame.init()
            if pygame.get_error():
                raise RuntimeError("Failed to initialize Pygame in game/init")
                
        except Exception as e:
            raise RuntimeError(f"Failed to initialize game in game/init: {str(e)}")
        
        self.m = 20
        self.n = 30
        if self.m <= 0 or self.n <= 0:
            raise ValueError("Invalid board dimensions in game/init")
        
        display_info = pygame.display.Info()
        self.max_screen_width = display_info.current_w
        self.max_screen_height = display_info.current_h
        self.windowed_width = self.n * 50 + 300  #+300 for status screen
        self.windowed_height = self.m * 50
        
        self.is_fullscreen = False
        self.screen_width = self.windowed_width
        self.screen_height = self.windowed_height
        self.board_width = self.n * 50
        self.board_height = self.m * 50

        try:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
            if not self.screen:
                raise RuntimeError("Failed to create game window in game/init")
                
            self.background = pygame.Surface(self.screen.get_size())
            if not self.background:
                raise RuntimeError("Failed to create background surface in game/init")
            
        except Exception as e:
            pygame.quit()
            raise RuntimeError(f"Failed to initialize display in game/init: {str(e)}")

        pygame.display.set_caption("Warbound")
        
        self.status_surface = pygame.Surface((300, self.screen_height))

        self.running = True
        

        # initialize the board
        self.board = Board(self.m, self.n, self.board_width, self.board_height, [])
        
        self.units1 = self._create_units(1)
        self.units2 = self._create_units(2)

        self.units1[0].has_general = True  
        self.units2[0].has_general = True

        self.board = Board(self.m, self.n, self.board_width, self.board_height, self._get_all_units())
        self.board_surface = pygame.Surface((self.board_width, self.board_height))
        self.selected_square = None
        
        self.selected_unit = None
        self.current_player = 1
        
        self.movement_points = {}  #tracks movement points for each unit
        self._reset_movement_points()
        
        self.game_over = False
        self.winner = None
        
        if not pygame.font.get_init():
            pygame.font.init()

        self.font = pygame.font.Font(None, 74)  #victory message
        self.small_font = pygame.font.Font(None, 36) #UI elements
        self.mini_font = pygame.font.Font(None, 24)  #status elements
        self._draw_board()
        self.menu = Menu(self.screen)
        self.state = "menu"

    def toggle_fullscreen(self):
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
            width_scale = game_area_width / (self.n * 50)
            height_scale = self.screen_height / (self.m * 50)
            scale = min(width_scale, height_scale)
            
            self.board_width = int(self.n * 50 * scale)
            self.board_height = int(self.m * 50 * scale)
        else:
            self.board_width = self.n * 50
            self.board_height = self.m * 50
        
        self.board_surface = pygame.Surface((self.board_width, self.board_height))
        self.status_surface = pygame.Surface((300, self.screen_height))
        self.board = Board(self.m, self.n, self.board_width, self.board_height, self._get_all_units())
    
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
            return self.units1
        else:
            return self.units2

    def _create_units(self, player):
        """
        Creates warriors and archers in the specified symmetric formation for the given player
        """
        units = []
        
        if player == 1:
            warrior_start_row = 6
            archer_start_col = 1
            warrior_col_start = 6
            left_archer_row_start = 1
            right_archer_row_start = 11  
        else:
            warrior_start_row = 6 
            archer_start_col = self.n - 4 
            warrior_col_start = self.n - 11
            left_archer_row_start = 11
            right_archer_row_start = 1 

        for row in range(8):
            for col in range(5):
                position = (warrior_start_row + row, warrior_col_start + col)
                warrior = Hoplite(position, player)
                warrior.terrain = self.board.terrain.get(position)
                units.append(warrior)

        for row in range(8):
            for col in range(3):
                position = (right_archer_row_start + row, archer_start_col + col)
                archer = Archer(position, player)
                archer.terrain = self.board.terrain.get(position)
                units.append(archer)
        
        for row in range(8):
            for col in range(3):
                position = (left_archer_row_start + row, archer_start_col + col)
                archer = Archer(position, player)
                archer.terrain = self.board.terrain.get((row, col))
                units.append(archer)
        
        return units
    
    def _get_all_units(self):

        """
        Returns a list of all units in the game
        """

        return self.units1 + self.units2
    
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
        self.board.draw(self.board_surface, self.board.selected_square)

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
        
    def _update_status_surface(self):

        """
        Updates the status surface
        """

        self.status_surface.fill((50, 50, 50))

        status_text = self.mini_font.render(f"Status", True, (255, 255, 255))
        self.status_surface.blit(status_text, (10, 10))
    
        if self.selected_unit:
            name_text = self.mini_font.render(f"Unit: {self.selected_unit.__class__.__name__}", True, (255, 255, 255))
            remaining_units_text = self.mini_font.render(f"Remaining Units: {self.selected_unit.remaining_units}", True, (255, 255, 255))
            attack_text = self.mini_font.render(f"Attack: {self.selected_unit.attack_points}", True, (255, 255, 255))
            defense_text = self.mini_font.render(f"Defense: {self.selected_unit.defense_points}", True, (255, 255, 255))
            formation_text = self.mini_font.render(f"Formation: {self.selected_unit.formation}", True, (255, 255, 255))
            change_formation_text = self.mini_font.render(f"Press 'G' to change formation", True, (255,255,255))
            action_text = self.mini_font.render(f"Action: {self.selected_unit.action} (Press 'F' to change)", True, (255, 255, 255))
            terrain_text = self.mini_font.render(f"Current terrain: {self.selected_unit.terrain}", True, (255, 255, 255))
                
            self.status_surface.blit(name_text, (10, 40))
            self.status_surface.blit(remaining_units_text, (10, 70))
            self.status_surface.blit(attack_text, (10, 100))
            self.status_surface.blit(defense_text, (10, 130))
            self.status_surface.blit(formation_text, (10,160))
            self.status_surface.blit(change_formation_text, (10, 190))
            self.status_surface.blit(action_text, (10, 220))
            self.status_surface.blit(terrain_text, (10, 250))
        else:
            no_unit_text = self.mini_font.render("Select a Unit", True, (255, 255, 255))
            self.status_surface.blit(no_unit_text, (10, 40))

    def _handle_general_movement(self, clicked_unit):

        """
        Handle movement of the general between units
        
        Args:
            clicked_unit (BaseUnit): The unit that was clicked
        
        Returns:
            bool: True if general movement was handled, False otherwise
        """

        if (self.selected_unit and 
            self.selected_unit.has_general and 
            self._can_general_move(self.selected_unit, clicked_unit)):
            
            self.selected_unit.has_general = False
            clicked_unit.has_general = True
            self.selected_unit = None
            self.board.select_square(None, 0)
            return True
        return False

    def _handle_unit_selection(self, clicked_unit, clicked_square):
        """
        Handle the selection of a unit
        """
        if clicked_unit and clicked_unit.player == self.current_player:
            if not self._handle_general_movement(clicked_unit):
                self.selected_unit = clicked_unit
                self.board.select_square(clicked_square, self.movement_points[clicked_unit])

                self.board.update_attack_overlays(clicked_unit, self._get_all_units())
            self._draw_board()
        else:
            self.selected_unit = None
            self.board.select_square(None, 0)
            self.board.update_attack_overlays(None, self._get_all_units())
            self._draw_board()

    def _handle_unit_movement(self, clicked_square):
        if not self.selected_unit:
            return

        target_unit = self._get_unit_at_position(clicked_square)
        
        if isinstance(self.selected_unit, Archer) and self.selected_unit.action == "Attack":
            if self.selected_unit.can_attack(clicked_square) and target_unit and target_unit.player != self.current_player:
                self._handle_combat(target_unit)
                self.movement_points[self.selected_unit] = 0
                self._update_unit_selection(self.selected_unit.position)
                return

        if isinstance(self.selected_unit, Hoplite):
            if target_unit and target_unit.player != self.current_player:
                if self.selected_unit.can_attack(clicked_square):
                    self._handle_combat(target_unit)
                    self.movement_points[self.selected_unit] = 0
                    self._update_unit_selection(self.selected_unit.position)
                    return

                elif clicked_square in self.board.reachable_positions:
                    movement_cost = self.board.movement_costs[clicked_square]
                    if self.movement_points[self.selected_unit] >= movement_cost:
                        self.selected_unit.move(clicked_square)
                        self.selected_unit.terrain = self.board.terrain.get(clicked_square)
                        self.movement_points[self.selected_unit] -= movement_cost
                        if self.selected_unit.can_attack(target_unit.position):
                            self._handle_combat(target_unit)
                            self.movement_points[self.selected_unit] = 0
                        self._update_unit_selection(clicked_square)
                        return

        if clicked_square in self.board.reachable_positions:
            movement_cost = self.board.movement_costs[clicked_square]
            if self.movement_points[self.selected_unit] >= movement_cost:
                self._execute_movement(clicked_square, movement_cost)
            
    def _execute_movement(self, target_square, movement_cost):

        """
        Execute the actual movement and potential combat
        
        Args:
            target_square (tuple): The target position
            movement_cost (int): Cost of the movement
        """

        target_unit = self._get_unit_at_position(target_square)

        if isinstance(self.selected_unit, Archer) and target_unit and target_unit.player != self.current_player:
            self._handle_combat(target_unit)
            self.movement_points[self.selected_unit] = 0
            return
        
        if target_unit and target_unit.player != self.current_player:
            self._handle_combat(target_unit)
            if self.selected_unit.is_alive:
                self.selected_unit.move(target_square)
                self.selected_unit.terrain = self.board.terrain.get(target_square)
                self.movement_points[self.selected_unit] = 0
            
        elif not target_unit:
            self.selected_unit.move(target_square)
            self.selected_unit.terrain = self.board.terrain.get(target_square)
            self.movement_points[self.selected_unit] -= movement_cost
        
        self._update_unit_selection(target_square)

    def _handle_combat(self, target_unit):

        """
        Handle combat between units
        
        Args:
            target_unit (BaseUnit): The unit being attacked
        """

        self.selected_unit.attack(target_unit)
        
        if target_unit.has_general and not target_unit.is_alive:
            self.game_over = True
            self.winner = self.current_player
        elif self.selected_unit.has_general and not self.selected_unit.is_alive:
            self.game_over = True
            self.winner = self.not_current_player

    def _update_unit_selection(self, new_position):

        """
        Update unit selection state after movement
        
        Args:
            new_position (tuple): The new position of the unit
        """

        if not self.selected_unit.is_alive:
            self.board.select_square(None, 0)
            self.selected_unit = None

        elif self.movement_points[self.selected_unit] <= 0:
            self.board.select_square(None, 0)
            self.selected_unit = None
        else:
            self.board.select_square(new_position, 
                                   self.movement_points[self.selected_unit])
        self._draw_board()

    def _handle_mouse_click(self, event, mouse_position):

        """
        Handle mouse click events
        
        Args:
            event (pygame.Event): The mouse event
            mouse_position (tuple): Position of the mouse click
        """

        mouse_x, mouse_y = mouse_position
        
        if self.is_fullscreen:
            board_y_offset = (self.screen_height - self.board_height) // 2
            mouse_y -= board_y_offset

        clicked_square = self.board.get_square_from_click((mouse_x, mouse_y), self.board_surface)
        if clicked_square is None:
            return

        if event.button == 1: 
            clicked_unit = self._get_unit_at_position(clicked_square)
            
            if clicked_unit and clicked_unit.player == self.current_player:
                self._handle_unit_selection(clicked_unit, clicked_square)
            else:
                self._handle_unit_movement(clicked_square)
                
        elif event.button == 3:  
            self.selected_unit = None
            self.board.select_square(None, 0)
            self._draw_board()

    def _handle_key_press(self, event):

        """
        Handle keyboard events, with only essential keys.
        
        Args:
            event (pygame.Event): The keyboard event
        """
        
        if event.key == pygame.K_SPACE:
            self._end_turn()
        elif event.key == pygame.K_g: 
            self.toggle_formation()
        elif event.key == pygame.K_f:
            self.toggle_action()

    def _end_turn(self):

        """
        Handle the end of a player's turn
        """

        self.not_current_player = self.current_player
        self.current_player = 3 - self.current_player
        self.selected_unit = None
        self.board.select_square(None, 0)
        self.board.update_attack_overlays(None, self._get_all_units())
        self._reset_movement_points()
        self._draw_board()

    def handle_events(self):
        
        """
        Handle main events
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                if not self.is_fullscreen:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    if self.state == "menu":
                        self.menu.handle_resize()
                    else:
                        self.toggle_fullscreen()  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  
                    self.toggle_fullscreen()
                    if self.state == "menu":
                        self.menu.handle_resize()
                elif self.state == "game" and not self.game_over:
                    self._handle_key_press(event)
            elif self.state == "game" and not self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_mouse_click(event, pygame.mouse.get_pos())


    
    def toggle_formation(self):

        """
        Changes the formation of a given unit if movement points > 0
        """
        if self.selected_unit:
            if self.movement_points[self.selected_unit] > 0:
                formations = list(self.selected_unit.formations.keys())
                current_index = formations.index(self.selected_unit.formation)
                next_index = (current_index + 1) % len(formations)
                next_formation = formations[next_index]
                self.selected_unit.change_formation(next_formation)

    def toggle_action(self):

        """
        Changes the action of a given unit
        """
        if self.selected_unit:
            current_index = self.selected_unit.actions.index(self.selected_unit.action)
            self.selected_unit.change_action(self.selected_unit.actions[1-current_index])

    
    def _can_general_move(self, from_unit, to_unit):

        """
        Check if the general can move between units
        
        Args:
            from_unit (BaseUnit): Unit the general is currently in
            to_unit (BaseUnit): Un:
            it the general wants to move to
            
        Returns:
            bool: True if movement is valid
        """

        if not from_unit.has_general or not to_unit.is_alive:
            return False
            
        if to_unit.player != self.current_player:
            return False
            
        row1, col1 = from_unit.position
        row2, col2 = to_unit.position
        return abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1
    
    def _get_all_units(self):

        """
        Gets all units in the game
        """

        return self.units1 + self.units2
    
    def render(self):

        """
        Renders the game screen with fullscreen support.
        """

        self.screen.fill((0, 0, 0))
        self.board_surface.fill((0, 0, 0))
        self.board.draw(self.board_surface, self.selected_square)

        for unit in self.units1 + self.units2:
            if unit.is_alive:
                unit.draw(self.board_surface, self.board)

        board_x = 0
        board_y = (self.screen_height - self.board_height) // 2 if self.is_fullscreen else 0
        self.screen.blit(self.board_surface, (board_x, board_y))
        
        self._draw_movement_points()
        self._update_status_surface()
        status_x = self.board_width
        self.screen.blit(self.status_surface, (status_x, 0))
        
        if self.game_over:
            self._draw_victory_message()
        
        pygame.display.flip()

    def _check_game_over(self):

        """
        Checks if a general has been killed
        """

        for player_units in [self.units1, self.units2]:
            has_general = False
            for unit in player_units:
                if unit.is_alive and unit.has_general:
                    has_general = True
                    break
            if not has_general:
                self.game_over = True
                self.winner = 2 if player_units == self.units1 else 1
                break
            

    def run(self):
        
        """
        R u n s.
        """

        try:
            while self.running:
                if self.state == "menu":
                    self.menu.draw()
                    new_state = self.menu.handle_events()

                    if new_state.startswith("game_map"):
                        self.state = "game"
                        map_choice = 1 if new_state == "game_map1" else 2
                        self.board = Board(self.m, self.n, self.board_width, self.board_height, self._get_all_units(), map_choice=map_choice)

                    elif new_state == "game":
                        self.state = "game"
                        if not self.menu.sound_enabled:
                            for unit in self._get_all_units():
                                unit.move_sound.set_volume(0)
                                unit.attack_sound.set_volume(0)
                        else:
                            for unit in self._get_all_units():
                                unit.move_sound.set_volume(self.menu.sound_volume)
                                unit.attack_sound.set_volume(self.menu.sound_volume)
                    elif new_state == "quit":
                        self.running = False

                elif self.state == "game":
                    self.handle_events()
                    self.update()
                    self.render()

        except Exception as e:
            print(f"Game crashed: {str(e)}")
        finally:
            pygame.quit()

    def update(self):

        """
        uga uga buga ugaga lbubleub
        """

        try:        
            self._draw_board()
                    
        except Exception as e:
            raise RuntimeError(f"Failed to draw the board: {str(e)}")
        
    def _draw_victory_message(self):

        """
        Draws the victory message
        """

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