"""
This module represents the main game structure, responsible for initializing, handling events, updating, and rendering the game.
"""

import pygame
from .board import Board
from .units.units import Hoplite, LightHorsemen, Viking, Archer, Crossbowman, Legionary, Hypaspist, HeavyCavalry, MenAtArms
from .units.constants import Formations
from .units.base_unit import Direction

class Game:
    def __init__(self, player1_general=None, player2_general=None, map_choice=1):
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
        
        self.state = "game"

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

        self.player1_general = player1_general
        self.player2_general = player2_general

        self.player1_formation = getattr(Formations, player1_general.lower(), Formations.default) if player1_general else Formations.default
        self.player2_formation = getattr(Formations, player2_general.lower(), Formations.default) if player2_general else Formations.default
        
        self.status_surface = pygame.Surface((300, self.screen_height))
        self.running = True

        self.map_choice = map_choice
        self.board = Board(self.m, self.n, self.board_width, self.board_height, [], map_choice=self.map_choice)
        
        self.units1 = self._create_units(1, self.player1_formation)
        self.units2 = self._create_units(2, self.player2_formation)
        
        self.units1[0].has_general = True
        self.units1[0].general_id = self.player1_general
        self.units2[0].has_general = True
        self.units2[0].general_id = self.player2_general

        self.board = Board(self.m, self.n, self.board_width, self.board_height, self._get_all_units(), map_choice=self.map_choice)
        self.board_surface = pygame.Surface((self.board_width, self.board_height))
        
        self.running = True
        self.selected_square = None
        self.selected_unit = None
        self.current_player = 1
        self.movement_points = {}  #tracks movement points for each unit
        self._reset_movement_points()
        self.game_over = False
        self.winner = None

        for unit in self._get_player_units(self.current_player):
            unit.has_attacked = False
        
        if not pygame.font.get_init():
            pygame.font.init()

        self.font = pygame.font.Font(None, 74)  #victory message
        self.small_font = pygame.font.Font(None, 36) #UI elements
        self.mini_font = pygame.font.Font(None, 24)  #status elements
        self._draw_board()


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
        self.board = Board(self.m, self.n, self.board_width, self.board_height, self._get_all_units(), map_choice=self.map_choice)
    
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

    
    def _create_units(self, player, board_layout):
        """
        Creates units based on a string layout.
        
        Args:
            player (int): Player number (1 or 2)
            board_layout (List[str]): List of strings representing the board layout
        
        Returns:
            List[BaseUnit]: List of created units
        """
        
        unit_mapping = {
        'H': Hoplite,
        'C': LightHorsemen,
        'P': HeavyCavalry,
        'V': Viking,
        'A': Archer,
        'B': Crossbowman,
        'I': Hypaspist,
        'L': Legionary,
        'M': MenAtArms,
        '#': None
        }

        units = []
        
        if player == 2:   #if player 2, flip the layout horizontally
            board_layout = [row[::-1] for row in board_layout]
        
        for row_idx, row in enumerate(board_layout):
            for col_idx, char in enumerate(row):
                if char in unit_mapping and char != '#':
                    unit_class = unit_mapping[char]
                    if player == 2:
                        position = (self.m - 1 - row_idx, col_idx)
                    else:
                        position = (row_idx, col_idx)
                    unit = unit_class(position, player)
                    unit.terrain = self.board.terrain.get(position)
                    units.append(unit)
        
        if units:
            units[0].has_general = True
            
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

    
    def _update_status_surface(self):

        """
        Updates the status surface with a modern, organized layout
        """

        BACKGROUND_TOP = (31, 41, 55)     
        BACKGROUND_BOTTOM = (17, 24, 39) 
        TEXT_COLOR = (229, 231, 235)    
        HEADER_COLOR = (252, 211, 77)    
        SECTION_BG = (31, 41, 55, 128)   
        
        PANEL_WIDTH = 300
        SECTION_PADDING = 15
        
        height = self.screen_height
        self.status_surface = pygame.Surface((PANEL_WIDTH, height), pygame.SRCALPHA)
        
        for y in range(height):
            progress = y / height
            r = BACKGROUND_TOP[0] + (BACKGROUND_BOTTOM[0] - BACKGROUND_TOP[0]) * progress
            g = BACKGROUND_TOP[1] + (BACKGROUND_BOTTOM[1] - BACKGROUND_TOP[1]) * progress
            b = BACKGROUND_TOP[2] + (BACKGROUND_BOTTOM[2] - BACKGROUND_TOP[2]) * progress
            pygame.draw.line(self.status_surface, (r, g, b), (0, y), (PANEL_WIDTH, y))

        y_offset = SECTION_PADDING

        header_font = pygame.font.Font(None, 48) 
        header_text = header_font.render("Unit Status", True, HEADER_COLOR)
        header_rect = header_text.get_rect(centerx=PANEL_WIDTH // 2, top=y_offset)
        self.status_surface.blit(header_text, header_rect)

        y_offset += header_rect.height + SECTION_PADDING

        turn_bg = pygame.Surface((PANEL_WIDTH - 40, 60), pygame.SRCALPHA)
        turn_bg.fill(SECTION_BG)
        self.status_surface.blit(turn_bg, (20, y_offset))

        turn_text = f"Player {self.current_player}'s Turn"
        turn_surface = self.small_font.render(turn_text, True, HEADER_COLOR)
        self.status_surface.blit(turn_surface, (30, y_offset + 10))

        space_text = "Press SPACE to end turn"
        space_surface = self.mini_font.render(space_text, True, TEXT_COLOR)
        self.status_surface.blit(space_surface, (30, y_offset + 35))

        y_offset += 80  
        
        y_offset += header_rect.height + SECTION_PADDING
        pygame.draw.line(self.status_surface, (75, 85, 99), (20, y_offset), (PANEL_WIDTH - 20, y_offset))
        y_offset += SECTION_PADDING

        if not self.selected_unit:
            no_unit_text = self.mini_font.render("No Unit Selected", True, TEXT_COLOR)
            no_unit_rect = no_unit_text.get_rect(centerx=PANEL_WIDTH // 2, top=y_offset)
            self.status_surface.blit(no_unit_text, no_unit_rect)
            return

        unit = self.selected_unit
    
        section_bg = pygame.Surface((PANEL_WIDTH - 40, 80), pygame.SRCALPHA)
        section_bg.fill(SECTION_BG)
        self.status_surface.blit(section_bg, (20, y_offset))
        
        type_text = self.small_font.render(unit.__class__.__name__, True, HEADER_COLOR)
        self.status_surface.blit(type_text, (30, y_offset + 10))
        
        hp_percent = (unit.current_hp / unit.max_hp) * 100
        hp_text = self.mini_font.render(f"HP: {hp_percent:.1f}%", True, TEXT_COLOR)
        self.status_surface.blit(hp_text, (30, y_offset + 40))
        
        pygame.draw.rect(self.status_surface, (75, 85, 99),(30, y_offset + 60, PANEL_WIDTH - 60, 8))
        
        hp_color = (34, 197, 94) if hp_percent > 70 else \
                (234, 179, 8) if hp_percent > 30 else \
                (239, 68, 68)
        hp_width = int((PANEL_WIDTH - 60) * (hp_percent / 100))
        pygame.draw.rect(self.status_surface, hp_color,
                        (30, y_offset + 60, hp_width, 8))
        
        y_offset += 100 

        section_bg = pygame.Surface((PANEL_WIDTH - 40, 120), pygame.SRCALPHA)
        section_bg.fill(SECTION_BG)
        self.status_surface.blit(section_bg, (20, y_offset))
        
        section_title = self.mini_font.render("COMBAT STATS", True, (156, 163, 175))
        self.status_surface.blit(section_title, (30, y_offset + 10))
        
        stats_y = y_offset + 40
        stats_data = [
            (f"Attack Points: {unit.attack_points}", (239, 68, 68)),
            (f"Defense Points: {unit.defense_points}", (59, 130, 246)),
            (f"Attack Range: {unit.attack_range}", (168, 85, 247))
        ]
        
        for text, color in stats_data:
            stat_text = self.mini_font.render(text, True, color)
            self.status_surface.blit(stat_text, (30, stats_y))
            stats_y += 25
            
        y_offset += 140 

        section_bg = pygame.Surface((PANEL_WIDTH - 40, 120), pygame.SRCALPHA)
        section_bg.fill(SECTION_BG)
        self.status_surface.blit(section_bg, (20, y_offset))
        
        section_title = self.mini_font.render("TACTICAL INFO", True, (156, 163, 175))
        self.status_surface.blit(section_title, (30, y_offset + 10))
        
        tactical_y = y_offset + 40
        tactical_data = [
            (f"Movement Points: {self.movement_points.get(unit, 0)}", TEXT_COLOR),
            (f"Formation: {unit.formation}", TEXT_COLOR),
            (f"Terrain: {unit.terrain}", TEXT_COLOR),
            (f"Facing: {Direction.to_string(self.selected_unit.facing_direction)}", TEXT_COLOR),
        ]
        
        for text, color in tactical_data:
            tact_text = self.mini_font.render(text, True, color)
            self.status_surface.blit(tact_text, (30, tactical_y))
            tactical_y += 25
            
        y_offset += 140

        section_bg = pygame.Surface((PANEL_WIDTH - 40, 160), pygame.SRCALPHA)
        section_bg.fill(SECTION_BG)
        self.status_surface.blit(section_bg, (20, y_offset))
        
        section_title = self.mini_font.render("ACTIVE MODIFIERS", True, (156, 163, 175))
        self.status_surface.blit(section_title, (30, y_offset + 10))
        
        mod_y = y_offset + 40

        y_offset += 160  
        pygame.draw.line(self.status_surface, (75, 85, 99), 
                        (20, y_offset), (PANEL_WIDTH - 20, y_offset))
        
        y_offset += 30  
        center_x = PANEL_WIDTH // 2
        compass_size = 70  #size is adjustable
        
        points = {
            Direction.NORTH: [(center_x, y_offset), 
                            (center_x + 15, y_offset + 35), 
                            (center_x, y_offset + 30),
                            (center_x - 15, y_offset + 35)],
            Direction.EAST: [(center_x + 50, y_offset + 50),
                           (center_x + 15, y_offset + 65),
                           (center_x + 20, y_offset + 50),
                           (center_x + 15, y_offset + 35)],
            Direction.SOUTH: [(center_x, y_offset + 100),
                            (center_x + 15, y_offset + 65),
                            (center_x, y_offset + 70),
                            (center_x - 15, y_offset + 65)],
            Direction.WEST: [(center_x - 50, y_offset + 50),
                           (center_x - 15, y_offset + 65),
                           (center_x - 20, y_offset + 50),
                           (center_x - 15, y_offset + 35)]
        }
        
        for direction, point_list in points.items():
            color = (252, 211, 77) if (self.selected_unit and 
                                     direction == self.selected_unit.facing_direction) else (229, 231, 235)
            pygame.draw.polygon(self.status_surface, color, point_list)

        pygame.draw.circle(self.status_surface, (55, 65, 81), 
                         (center_x, y_offset + 50), 3)
        pygame.draw.circle(self.status_surface, (252, 211, 77), 
                         (center_x, y_offset + 50), 3, 1)
        
        direction_labels = [
            (Direction.NORTH, "N", center_x, y_offset - 10),
            (Direction.EAST, "E", center_x + 60, y_offset + 55),
            (Direction.SOUTH, "S", center_x, y_offset + 110),
            (Direction.WEST, "W", center_x - 60, y_offset + 55)
        ]

        for direction, label, x, y in direction_labels:
            color = (252, 211, 77) if (self.selected_unit and 
                                    direction == self.selected_unit.facing_direction) else (229, 231, 235)
            text = self.small_font.render(label, True, color)
            text_rect = text.get_rect(center=(x, y))
            self.status_surface.blit(text, text_rect)
        
        formation_mods = unit.formations.get(unit.formation, {})
        
        attack_mod = (formation_mods.get('attack_modifier', 1.0) - 1) * 100
        if attack_mod != 0:
            mod_text = f"{'+' if attack_mod > 0 else ''}{attack_mod:.0f}% Attack (Formation)"
            mod_color = (34, 197, 94) if attack_mod > 0 else (239, 68, 68)
            mod_surface = self.mini_font.render(mod_text, True, mod_color)
            self.status_surface.blit(mod_surface, (30, mod_y))
            mod_y += 25
            
        defense_mod = (formation_mods.get('defense_modifier', 1.0) - 1) * 100
        if defense_mod != 0:
            mod_text = f"{'+' if defense_mod > 0 else ''}{defense_mod:.0f}% Defense (Formation)"
            mod_color = (34, 197, 94) if defense_mod > 0 else (239, 68, 68)
            mod_surface = self.mini_font.render(mod_text, True, mod_color)
            self.status_surface.blit(mod_surface, (30, mod_y))
            mod_y += 25
            
        if unit.terrain == "mountain":
            if unit.attack_type == "melee":
                mod_text = "+50% Defense vs Melee (Mountain)"
                mod_surface = self.mini_font.render(mod_text, True, (34, 197, 94))
                self.status_surface.blit(mod_surface, (30, mod_y))
                mod_y += 25
            else:
                mod_text = "+20% Defense vs Ranged (Mountain)"
                mod_surface = self.mini_font.render(mod_text, True, (34, 197, 94))
                self.status_surface.blit(mod_surface, (30, mod_y))
                mod_y += 25
        elif unit.terrain == "forest":
            if unit.attack_type == "ranged":
                mod_text = "+70% Defense vs Ranged (Forest)"
                mod_surface = self.mini_font.render(mod_text, True, (34, 197, 94))
                self.status_surface.blit(mod_surface, (30, mod_y))
                mod_y += 25
            else:
                mod_text = "+25% Defense vs Melee (Forest)"
                mod_surface = self.mini_font.render(mod_text, True, (34, 197, 94))
                self.status_surface.blit(mod_surface, (30, mod_y))

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
        if clicked_unit and clicked_unit.player == self.current_player:
            if not self._handle_general_movement(clicked_unit):
                self.selected_unit = clicked_unit
                self.board.selected_square = clicked_square  
                self.board.select_square(clicked_square, self.movement_points[clicked_unit])
                self.board.update_attack_overlays(clicked_unit, self._get_all_units())
            self._draw_board()
        else:
            self.selected_unit = None
            self.board.selected_square = None 
            self.board.select_square(None, 0)
            self.board.update_attack_overlays(None, self._get_all_units())
            self._draw_board()

    def _handle_unit_movement(self, clicked_square):
        if not self.selected_unit:
            return

        target_unit = self._get_unit_at_position(clicked_square)
        
        if isinstance(self.selected_unit, (Archer, Crossbowman)):
            if self.selected_unit.can_attack(clicked_square) and \
                target_unit and target_unit.player != self.current_player and \
                not self.selected_unit.has_attacked:
                self._handle_combat(target_unit)
                self.movement_points[self.selected_unit] = 0
                self._update_unit_selection(self.selected_unit.position)
                return

        if isinstance(self.selected_unit, (Hoplite, LightHorsemen, HeavyCavalry, Viking, Hypaspist, Legionary)):
            if target_unit and target_unit.player != self.current_player:
                if self.selected_unit.can_attack(clicked_square) and \
                    not self.selected_unit.has_attacked:
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
                        if self.selected_unit.can_attack(target_unit.position) and\
                            not self.selected_unit.has_attacked:
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

        self.selected_unit.attack(target_unit, self.board)
        
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

        elif self.selected_unit and not self.selected_unit.has_changed_direction:
            if event.key == pygame.K_UP:
                self.selected_unit.change_direction(Direction.NORTH)
            elif event.key == pygame.K_RIGHT:
                self.selected_unit.change_direction(Direction.EAST)
            elif event.key == pygame.K_DOWN:
                self.selected_unit.change_direction(Direction.SOUTH)
            elif event.key == pygame.K_LEFT:
                self.selected_unit.change_direction(Direction.WEST)

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

        for unit in self._get_player_units(self.current_player):
            unit.has_attacked = False
            unit.reset_direction_change()

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
                    self.toggle_fullscreen()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_r and self.game_over:
                    self._restart_game()
                elif event.key == pygame.K_m and self.game_over:
                    self.running = False 
                else:
                    self._handle_key_press(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
        Runs the game.
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
        Updates
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
        
        instructions = "Press R to restart or M to return to menu"
        instructions_surface = self.small_font.render(instructions, True, (255, 255, 255))
        
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 20))
        instructions_rect = instructions_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 40))
        
        total_height = text_rect.height + instructions_rect.height + 60
        max_width = max(text_rect.width, instructions_rect.width) + 40

        background_surface = pygame.Surface((max_width, total_height))
        background_surface.fill((0, 0, 0))
        background_surface.set_alpha(128)  #adjustable transparency
        
        background_rect = background_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        self.screen.blit(background_surface, background_rect)
        self.screen.blit(text_surface, text_rect)
        self.screen.blit(instructions_surface, instructions_rect)

    def _restart_game(self):
        """
        Resets the game state for a new game
        """
        self.running = True
        self.units1 = self._create_units(1, self.player1_formation)
        self.units2 = self._create_units(2, self.player2_formation)
        self.units1[0].has_general = True
        self.units2[0].has_general = True
        self.board = Board(self.m, self.n, self.board_width, self.board_height, self._get_all_units(), map_choice=self.map_choice)
        self.selected_square = None
        self.selected_unit = None
        self.current_player = 1
        self.movement_points = {}
        self._reset_movement_points()
        self.game_over = False
        self.winner = None

        for unit in self._get_player_units(self.current_player):
            unit.has_attacked = False
        
        self._draw_board()