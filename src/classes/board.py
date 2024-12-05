"""
This module represents the game board, responsible for managing selectable squares, colors, and the highlighting system.
"""

import pygame
from .graph import BoardGraph
from .units.constants import Paths, Maps, Colors

class Board:
    
    """
    Manages the board layout, including the selection of squares, highlighting reachable positions, 
    and drawing the board on the screen.

    Attributes:
        m (int): Number of rows on the board.
        n (int): Number of columns on the board.
        initial_width (int): Initial width of the game window.
        initial_height (int): Initial height of the game window.
        selected_square (tuple or None): The currently selected square on the board, or None if no square is selected.
        terrain (dict): Dictionary mapping board coordinates to terrain types.
        units (list): List of game units on the board.
        graph (BoardGraph): Instance of the BoardGraph class to manage board connectivity.
        reachable_positions (set): Set of squares that are reachable from the selected square.
        sprites (dict): Terrain sprite dictionary.
        dangerous_squares (set): Squares within enemy attack range.
        attackable_squares (set): Squares containing attackable enemy units.

    Methods:
        _is_valid_position(row, col): Checks if a position is within the board boundaries.
        update_attack_overlays(selected_unit, all_units): Updates the dangerous and attackable squares
        get_square_from_click(mouse_pos, screen): Determines which square was clicked based on mouse position.
        select_square(square, movement_points): Selects a square and calculates reachable positions based on movement points.
        initialize_terrain(terrain_map): Initializes the terrain map from a provided map string.
        draw(screen, selected_square): Draws the board, with highlights for reachable and selected squares.
    """


    def __init__(self, m, n, initial_width, initial_height, units, map_choice=None) -> None:
        if map_choice == 1:
            self.terrain_map = Maps.map1
        elif map_choice == 2:
            self.terrain_map = Maps.map2
        else:
            self.terrain_map = Maps.map1 
            
        self.m = m
        self.n = n
        if m <= 0 or n <= 0:
            raise ValueError("Board dimensions must be positive integers in board/init")
        if initial_width <= 0 or initial_height <= 0:
            raise ValueError("Initial window dimensions must be positive in board/init")
        
        self.board_width = initial_width
        self.board_height = initial_height
        
        self.initial_width = initial_width
        self.initial_height = initial_height
        self.selected_square = None
        self.terrain = self.initialize_terrain(self.terrain_map)
        self.units = units
        self.graph = BoardGraph(m, n, self.terrain, units)
        self.reachable_positions = set()
        self.is_fullscreen = False

        self.sprites = {
            "plains": pygame.image.load(Paths.PLAIN_SPRITE).convert_alpha(),
            "mountain": pygame.image.load(Paths.MOUNTAIN_SPRITE).convert_alpha(),
            "forest": pygame.image.load(Paths.FOREST_SPRITE).convert_alpha(),
            "attackable": pygame.image.load(Paths.ATTACKABLE_SQUARE).convert_alpha(),
            "dangerous": pygame.image.load(Paths.DANGEROUS_SQUARE).convert_alpha()
        }

        self.dangerous_squares = set()
        self.attackable_squares = set()

    def _is_valid_position(self, row: int, col: int) -> bool:
        """
        Checks if a position is within the board boundaries.
        
        Args:
            row (int): Row index to check
            col (int): Column index to check
            
        Returns:
            bool: True if position is valid, False otherwise
        """
        return 0 <= row < self.m and 0 <= col < self.n
    
    def update_attack_overlays(self, selected_unit, all_units):

        """
        Updates the dangerous and attackable squares based on the selected unit
        and enemy positions. Only marks squares as dangerous if they are both:
        - Within the selected unit's movement range
        - Within an enemy unit's attack range

        Args:
            selected_unit (Unit): Currently selected game unit.
            all_units (list): List of all units in the game.
        """

        self.dangerous_squares.clear()
        self.attackable_squares.clear()
        
        if not selected_unit:
            return
                
        enemy_units = [unit for unit in all_units if unit.is_alive and unit.player != selected_unit.player]
        
        all_dangerous = set()
        for enemy in enemy_units:
            row, col = enemy.position
            attack_range = enemy.attack_range
            
            for i in range(-attack_range, attack_range + 1):
                for j in range(-attack_range, attack_range + 1):
                    new_row, new_col = row + i, col + j
                    if (self._is_valid_position(new_row, new_col) and 
                        abs(i) + abs(j) <= attack_range and
                        (new_row, new_col) != enemy.position): 
                        all_dangerous.add((new_row, new_col))
        
        self.dangerous_squares = all_dangerous.intersection(self.reachable_positions)
    
        for enemy in enemy_units:
            enemy_pos = enemy.position
            if selected_unit.can_attack(enemy_pos):
                self.attackable_squares.add(enemy_pos)


    def get_square_from_click(self, mouse_pos, screen):
        """Determines clicked square based on current board dimensions."""
        x, y = mouse_pos
        
        if self.is_fullscreen:
            board_y_offset = (screen.get_height() - self.board_height) // 2
            
            adjusted_y = y - board_y_offset
            
            if (x < 0 or x > self.board_width or 
                adjusted_y < 0 or adjusted_y > self.board_height):
                return None

            square_width = self.board_width / self.n
            square_height = self.board_height / self.m

            row = int(adjusted_y / square_height)
            col = int(x / square_width)
        else:
            square_width = self.initial_width / self.n
            square_height = self.initial_height / self.m
            
            row = int(y / square_height)
            col = int(x / square_width)

        if 0 <= row < self.m and 0 <= col < self.n:
            return row, col
        return None

    def select_square(self, square, movement_points, units=None) -> None:
        if movement_points < 0:
            raise ValueError("Negative movement points in board/select_square")
        
        if units is not None:
            self.units = units 

        self.selected_square = square
        if square is not None:
            if not isinstance(square, tuple) or len(square) != 2:
                raise ValueError("Invalid square format")
            
            row, col = square
            if not (0 <= row < self.m and 0 <= col < self.n):
                raise ValueError("Square position out of bounds in board/select_square")
            
        if square:
            self.reachable_positions, self.movement_costs = self.graph.get_reachable_positions(square, movement_points, self.units)
        else:
            self.reachable_positions = set()
            self.movement_costs = {}

    def initialize_terrain(self, terrain_map):

        """
        Initializes the terrain map from a provided map string.

        Args:
            terrain_map (str): A string representation of the terrain map where each line corresponds to a row 
            and each character represents a type of terrain. The expected characters are:
                - '#' for plains
                - '.' for mountains
                - 'x' for forests

        Returns:
            dict: A dictionary representing the terrain map, where:
                - Keys are tuples (row_index, col_index) indicating the row and column of each cell.
                - Values are strings representing the terrain type at each coordinate ("plains", "mountains" and "forests").
        
        Raises:
            ValueError: If an unexpected terrain character is encountered.
        """

        terrain = {}
        rows = [row.strip() for row in terrain_map.strip().split("\n")]

        for row_index, row in enumerate(rows):
            for col_index, cell in enumerate(row):
                if cell == "#":
                    terrain[(row_index, col_index)] = "plains"
                elif cell == ".":
                    terrain[(row_index, col_index)] = "mountain"
                elif cell == "x":
                    terrain[(row_index, col_index)] = "forest"
                else:
                    raise ValueError(f"Unexpected terrain character: {cell}")
        
        return terrain
        

    def draw(self, screen, selected_square=None):

        """
        Draws the board, with highlights for reachable and selected squares.
        
        Args:
            screen (pygame.Surface): Surface to draw the board on
            selected_square (tuple or None): Currently selected square coordinates

        Raises:
            ValueError: If screen surface or dimensions are invalid.
        """
        
        if not screen:
            raise ValueError("Invalid screen surface in board/draw")
                
        width, height = screen.get_size()
        if width <= 0 or height <= 0:
            raise ValueError("Invalid screen dimensions in board/draw")
        
        width, height = screen.get_size()
        square_width = width // self.n
        square_height = height // self.m

        for row in range(self.m):
            for column in range(self.n):

                # First plains, then the rest
                plains_sprite = self.sprites["plains"]
                plains_sprite_scaled = pygame.transform.scale(plains_sprite, (square_width, square_height))
                screen.blit(plains_sprite_scaled, (column * square_width, row * square_height))

                if self.terrain[(row, column)] == "mountain":
                    mountain_sprite = self.sprites["mountain"]
                    mountain_sprite_scaled = pygame.transform.scale(mountain_sprite, (square_width, square_height))
                    screen.blit(mountain_sprite_scaled, (column * square_width, row * square_height))
                
                if self.terrain[(row, column)] == "forest":
                    forest_sprite = self.sprites["forest"]
                    forest_sprite_scaled = pygame.transform.scale(forest_sprite, (square_width, square_height))
                    screen.blit(forest_sprite_scaled, (column * square_width, row * square_height))

                if (row, column) in self.reachable_positions:
                    highlight_surface = pygame.Surface((square_width, square_height), pygame.SRCALPHA)
                    pygame.draw.rect(highlight_surface, Colors.COLOR_HIGHLIGHT, (0, 0, square_width, square_height))
                    screen.blit(highlight_surface, (column * square_width, row * square_height))
       
                square_pos = (row, column)

                if square_pos in self.dangerous_squares:
                    dangerous_sprite = pygame.transform.scale(
                        self.sprites["dangerous"],
                        (square_width, square_height)
                    )
                    dangerous_sprite.set_alpha(128)  # 50% transparency
                    screen.blit(dangerous_sprite, 
                              (column * square_width, row * square_height))
                
                if square_pos in self.attackable_squares:
                    attackable_sprite = pygame.transform.scale(
                        self.sprites["attackable"],
                        (square_width, square_height)
                    )
                    attackable_sprite.set_alpha(128)  # 50% transparency
                    screen.blit(attackable_sprite, 
                              (column * square_width, row * square_height))